import subprocess
import os
import sys
import requests
import json
import threading
import time
import re
import psutil
from typing import Tuple, List
import signal
from pathlib import Path
import os
import platform
from log.logger_config import get_logger
from .FileContentManager import FileContentManager
from .ConfigAgent import ConfigAgent
from .TaskErrorPlanner import TaskErrorPlanner
from .ErrorDetection import ErrorDetection


logger = get_logger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.BugExplainer import BugExplainer
from fsd.coding_agent.SelfHealingAgent import SelfHealingAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.coding_agent.FileManagerAgent import FileManagerAgent
from fsd.util.utils import parse_payload

class CompileCommandRunner:
    def __init__(self, repo):
        """
        Initializes the CommandRunner.
        """
        self.repo = repo
        self.config = ConfigAgent(repo)
        self.errorDetection = ErrorDetection(repo)
        self.errorPlanner = TaskErrorPlanner(repo)
        self.self_healing = SelfHealingAgent(repo)
        self.bugExplainer = BugExplainer(repo)
        self.project = ProjectManager(repo)
        self.fileManager = FileManagerAgent(repo)
        self.config_manager = FileContentManager(repo)  # Initialize CodeManager in the constructor
        self.directory_path = repo.get_repo_path()
        self.max_retry_attempts = 3  # Set a maximum number of retry attempts

    async def get_config_requests(self, instructions, file_name):
        """Generate coding requests based on instructions and context."""

        main_path = file_name
        logger.info(f" #### `ConfigAgent` is processing file: {file_name} in {main_path}")
        logger.info(f" #### Task: {instructions}")
        result = await self.config.get_config_requests(instructions, main_path)
        if main_path:
            await self.config_manager.handle_coding_agent_response(main_path, result)
            logger.info(f" #### `ConfigAgent` has completed its work on {file_name}")
        else:
            logger.debug(f" #### `ConfigAgent` was unable to locate the file: {file_name}")

    async def get_error_planner_requests(self, error, config_context, os_architecture, compile_files, original_prompt_language):
        """Generate coding requests based on instructions and context."""
        result = await self.errorPlanner.get_task_plans(error, config_context, os_architecture, compile_files, original_prompt_language)
        return result
    
    def run_command(self, command: str, is_localhost_command: str, method: str = 'bash', inactivity_timeout: int = 7, use_timeout: bool = True) -> Tuple[int, List[str]]:
        """
        Runs a given command using the specified method.
        Shows real-time output during execution within a Bash markdown block.
        Returns a tuple of (return_code, all_output).
        Implements an optional inactivity timeout to determine command completion.
        
        Parameters:
        - command (str): The shell command to execute.
        - method (str): The shell method to use (default is 'bash').
        - inactivity_timeout (int): Seconds to wait for new output before considering done.
        - use_timeout (bool): Whether to enforce the inactivity timeout.
        """
        # Give more time for install commands and package managers
        if is_localhost_command == "0" and any(cmd_keyword in command for cmd_keyword in ['install', 'update', 'upgrade']):
            inactivity_timeout = 120  # 2 minutes for installation commands
        elif is_localhost_command == "1":
            inactivity_timeout = 7
        else:
            inactivity_timeout = 5
    
        markdown_block_open = False  # Flag to track if markdown block is open
        process = None  # Initialize process variable

        try:
            # Use bash for all commands
            shell = True
            executable = '/bin/bash'

            # Check if the command is a 'cd' command
            if command.startswith('cd '):
                # Extract directory path and handle both quoted and unquoted paths
                new_dir = command[3:].strip()
                if (new_dir.startswith("'") and new_dir.endswith("'")) or (new_dir.startswith('"') and new_dir.endswith('"')):
                    new_dir = new_dir[1:-1]  # Remove quotes if present
                
                try:
                    os.chdir(new_dir)
                    logger.info(
                        f"#### Directory Change\n"
                        f"```bash\nChanged directory to: {new_dir}\n```\n"
                        f"----------------------------------------"
                    )
                    return 0, [f"Changed directory to: {new_dir}"]
                except Exception as e:
                    error_msg = f"Failed to change directory: {str(e)}"
                    logger.error(error_msg)
                    return 1, [error_msg]

            # Log the current working directory and the command to be executed
            current_path = os.getcwd()
            logger.info(
                f"#### Executing Command\n"
                f"```bash\n{command}\n```\n"
                f"**In Directory:** `{current_path}`\n"
                f"#### Command Output\n```bash"
            )
            markdown_block_open = True  # Code block is now open

            # Start the process in a new session to create a new process group
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=current_path,  # Explicitly set the working directory
                start_new_session=True  # Start the process in a new session
            )

            # Use psutil to handle process and its children
            parent = psutil.Process(process.pid)

            # Initialize output list
            output = []

            # Variable to track the last time output was received
            last_output_time = time.time()

            # Lock for thread-safe updates to last_output_time
            lock = threading.Lock()

            # Function to read output
            def read_output(stream, output_list):
                nonlocal markdown_block_open, last_output_time
                for line in iter(stream.readline, ''):
                    line = line.rstrip()
                    output_list.append(line)
                    logger.info(line)
                    with lock:
                        last_output_time = time.time()
                stream.close()

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_output, args=(process.stdout, output))
            stderr_thread = threading.Thread(target=read_output, args=(process.stderr, output))
            stdout_thread.start()
            stderr_thread.start()

            # Monitoring loop
            while True:
                if process.poll() is not None:
                    # Process has finished
                    break
                if use_timeout:
                    with lock:
                        time_since_last_output = time.time() - last_output_time
                    if time_since_last_output > inactivity_timeout:
                        # No output received within the inactivity timeout
                        logger.info(f"No output received for {inactivity_timeout} seconds. Assuming command completion.")
                        break
                time.sleep(0.1)  # Prevent busy waiting

            # If the process is still running, attempt to terminate it gracefully
            if process.poll() is None:
                try:
                    logger.info(f"Attempting to terminate the subprocess after inactivity timeout of {inactivity_timeout} seconds.")
                    # Terminate the subprocess
                    process.terminate()

                    try:
                        process.wait(timeout=5)
                        logger.info("Subprocess terminated gracefully.")
                    except subprocess.TimeoutExpired:
                        logger.info("Subprocess did not terminate in time; killing it.")
                        process.kill()

                except Exception as e:
                    logger.error(f"Error terminating the subprocess: {e}")

            # Wait for threads to finish reading
            stdout_thread.join()
            stderr_thread.join()

            # Close the markdown code block if it's open
            if markdown_block_open:
                logger.info("```")  # Close the markdown block
                markdown_block_open = False

            return_code = process.returncode
            logger.info(
                f"#### Command Finished.\n"
                f"----------------------------------------"
            )
            logger.info("The `CommandRunner` has completed the current step and is proceeding to the next one.")
            return return_code, output

        except Exception as e:
            logger.error(f"An error occurred while running the command: {e}")
            # Ensure that the subprocess is terminated in case of an exception
            if process and process.poll() is None:
                try:
                    logger.info("Attempting to terminate the subprocess due to an exception.")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.info("Subprocess did not terminate in time; killing it.")
                        process.kill()
                except Exception as terminate_error:
                    logger.error(f"Failed to terminate subprocess after exception: {terminate_error}")
            return -1, [f"An error occurred: {e}"]

    def update_file(self, file_name, content):
        """
        Updates the content of a file.
        """
        try:
            with open(file_name, 'a') as file:
                file.write(content + '\n')
            logger.info(f" #### `FileUpdater` has successfully updated {file_name}")
            return f"Successfully updated {file_name}"
        except Exception as e:
            logger.error(f"  `FileUpdater` failed to update {file_name}: {str(e)}")
            return f"Failed to update {file_name}: {str(e)}"
        
    def open_terminal(self, bash_commands):
        """
        Opens a terminal window, navigates to the project path, and runs the specified bash commands.

        Parameters:
            bash_commands (list): List of bash commands to execute in the terminal.
        """
        # Join commands with && to run sequentially
        bash_command = " && ".join(bash_commands)

        # Retrieve the project path
        project_path = self.repo.get_repo_path()
        logger.info(f"#### Project Path: `{project_path}`")
        logger.info(f" #### Bash Commands: `{bash_command}`")

        # Ensure the project path exists
        if not Path(project_path).exists():
            logger.error(f"The project path does not exist: {project_path}")
            raise FileNotFoundError(f"The project path does not exist: {project_path}")

        # Detect the operating system
        current_os = platform.system()
        logger.info(f" #### Operating System Detected: {current_os}")

        try:
            if current_os == 'Windows':
                self._open_terminal_windows(project_path, bash_command)
            elif current_os == 'Darwin':
                self._open_terminal_mac(project_path, bash_command)
            else:
                logger.error(f"Unsupported Operating System: {current_os}")
                raise NotImplementedError(f"OS '{current_os}' is not supported.")
        except Exception as e:
            logger.exception(f"Failed to open terminal: {e}")
            raise

    def _open_terminal_windows(self, project_path, bash_command):
        """
        Opens Command Prompt on Windows, navigates to the project path, and runs the bash command.

        Parameters:
            project_path (str): The path to navigate to.
            bash_command (str): The command to execute.
        """
        # Construct the command to open cmd.exe, change directory, and execute the bash command
        # The /k flag keeps the window open after the command executes
        cmd = f'start cmd.exe /k "cd /d "{project_path}" && {bash_command}"'
        logger.debug(f"Windows CMD Command: {cmd}")

        # Execute the command
        subprocess.Popen(cmd, shell=True)
        logger.info("#### `Command Prompt` opened successfully.")

    def _open_terminal_mac(self, project_path, bash_command):
        """
        Opens Terminal.app on macOS, navigates to the project path, and runs the bash command.

        Parameters:
            project_path (str): The path to navigate to.
            bash_command (str): The command to execute.
        """
        # AppleScript to open a new Terminal window, navigate to the directory, and run the command
        apple_script = f'''
        tell application "Terminal"
            activate
            do script "cd \\"{project_path}\\"; {bash_command}"
        end tell
        '''
        logger.debug(f"AppleScript: {apple_script}")

        # Execute the AppleScript
        subprocess.Popen(['osascript', '-e', apple_script])
        logger.info("#### `Terminal.app` opened successfully.")

    async def print_code_error(self, error_message, code_files, role="Elite software engineer", max_retries=50):
        """
        Prints the code syntax error details.
        """
        totalfile = set()
        fixing_related_files = set()

        retries = 0

        while retries < max_retries:
            self.self_healing.clear_conversation_history()
            self.bugExplainer.clear_conversation_history()

            self.bugExplainer.initial_setup(role)
            self.self_healing.initial_setup(role)

            try:
                logger.info(" #### `ErrorHandler` has detected an issue and will commence work on the fix immediately")
                overview = ""

                overview = self.repo.print_tree()

                # Ensure basename list is updated without duplicates
                fixing_related_files.update(list(code_files))
                fixing_related_files.update(list(totalfile))

                logger.info(" #### `BugExplainer` is initiating the examination of bugs and creation of a fixing plan")
                fix_plans = await self.bugExplainer.get_bugFixed_suggest_requests(
                    error_message, list(fixing_related_files), overview)
                print(f"fix_plans: {fix_plans}")
                logger.info(" #### `BugExplainer` has completed the examination of bugs and creation of a fixing plan")

                logger.info(" #### `FileProcessor` is beginning work on file processing")
                file_result = await self.get_file_planning(fix_plans)
                await self.process_creation(file_result)
                add = file_result.get('Adding_new_files', [])
                move = file_result.get('Moving_files', [])
                if add or move:
                    commits = file_result.get('commits', "")
                    if commits:
                        self.repo.add_all_files(f"Zinley - {commits}")
                logger.info(" #### `FileProcessor` has completed processing files")

                logger.info(f" #### `FixingAgent` is attempting to fix for the {retries + 1} time")
                steps = fix_plans.get('steps', [])

                for step in steps:
                    file_name = step['file_name']
                    totalfile.add(file_name)

                await self.self_healing.get_fixing_requests(steps)

                # If we reach this point without exceptions, we assume the fix was successful
                logger.info(" #### `FixingAgent` has successfully applied the fix")
                return list(totalfile)

            except requests.exceptions.HTTPError as http_error:
                if http_error.response.status_code == 429:
                    wait_time = 2 ** retries
                    logger.info(f" #### `RateLimitHandler` has detected that the rate limit has been exceeded, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)  # Exponential backoff
                else:
                    logger.error(f"  `HTTPErrorHandler` encountered an HTTP error: {http_error}")
                    raise
            except Exception as e:
                logger.error(f"  `ErrorHandler` encountered an error during the fixing process: {str(e)}")

            retries += 1

        self.self_healing.clear_conversation_history()
        self.bugExplainer.clear_conversation_history()
        logger.info(" #### `BuildManager` reports that the build has failed after maximum retries")

    async def execute_steps(self, steps_json, compile_files, code_files, original_prompt_language):
        """
        Executes a series of steps provided in JSON format.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        self.errorDetection.initial_setup()
        steps = steps_json['steps']
        bash_commands = []

        for step in steps:
            is_localhost_command = step.get('is_localhost_command', "0")
            if step['method'] == 'bash':
                logger.info(f" #### `Compile Command Runner`: {step['prompt']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f" #### `Compile Command Runner`:")
                logger.info(f"```yaml\n{step['prompt']}\n```")

            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
            user_permission = input()

            user_prompt, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
            user_prompt = user_prompt.lower()

            if user_prompt == 'exit':
                logger.info(" #### The user has chosen to exit. The `CommandRunner` is halting execution.")
                return "Execution stopped by user"
            elif user_prompt == 's':
                logger.info(" #### The user has chosen to skip this step.")
                continue

            logger.info(f" #### `StepExecutor`: Executing step: {step['prompt']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    return_code, command_output = self.run_command(step['command'], is_localhost_command)

                    # Check for errors based on the return code
                    if return_code != 0 and return_code != None:
                        error_message = ','.join(command_output)
                        logger.error(f"  `CommandExecutor` failed with return code {return_code}: {error_message}")

                        # Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f"#### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                            user_choice = input()

                            user_select, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                            user_select = user_select.lower()
                            
                            if user_select == 'a':
                                logger.info(f" #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command, is_localhost_command)
                                if return_code == 0 or return_code == None:
                                    if is_localhost_command == "1" or is_localhost_command == 1 or is_localhost_command == None:
                                        logger.info(
                                            f"#### `Command agent` believes this is localhost `{suggested_command}`. "
                                            "It has run successfully, so there is potentially no error. "
                                            "However, I have already shut it down. We can open it separately in your terminal."
                                        )
                                        logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                                        user_run = input()

                                        user_select_run, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                                        user_select_run = user_select_run.lower()
                                        if user_select_run == 'a':
                                            bash_commands.append(suggested_command)
                                            self.open_terminal(bash_commands)
                                        break
                                    else:
                                        bash_commands.append(step['command'])
                                        break
                                else:
                                    # Update error_message with new command output
                                    error_message = ','.join(command_output)
                                    logger.error(
                                        f"\n #### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                            elif user_select == 'exit':
                                logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                            else:
                                logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")

                        error_check = await self.errorDetection.get_task_plan(error_message)
                        error_type = error_check.get('error_type', 1)
                        AI_error_message = error_check.get('error_message', "")

                        if error_type == 3:
                            logger.info("#### I apologize, but I'm having trouble understanding the issue. This could be due to missing context or unclear dependencies. Let me help you narrow it down:")
                            logger.info("##### 1. Select `Dependency Issue` if you suspect missing or incompatible dependencies")
                            logger.info("##### 2. Select `Code Logic Error` if you think there's a problem with the code implementation")
                            logger.info("##### 3. Select `Exit` if you'd prefer to skip this error\n")
                            logger.info("#### Please choose an option so I can better assist you with resolving this error. If you're unsure, option 1 is a good place to start.\n")
                    

                            logger.info("### Agent is confused due to lack of context. Please select 'Dependency Issue', 'Code Logic Error', or 'Exit' to help me better assist you: ")

                            user_prompt_json1 = input()
                            user_prompt1, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_prompt_json1)
                            user_prompt1 = user_prompt1.lower()

                            if user_prompt1 == "sy":
                                await self.print_code_error(AI_error_message, code_files)
                                retry_count += 1
                                continue  # Re-run the command after fixing the code error
                            elif user_prompt == "de":
                                # Proceed to handle the error
                                fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files, original_prompt_language)
                                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files, original_prompt_language)
                                if fixing_result == "Execution stopped by user":
                                    return "Execution stopped by user"
                                retry_count += 1
                            elif user_prompt == "exit":
                                logger.info(" #### User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                        elif error_type == 1:
                            await self.print_code_error(AI_error_message, code_files)
                            retry_count += 1
                            continue  # Re-run the command after fixing the code error
                        elif error_type == 2:
                             # Proceed to handle the error
                            fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files, original_prompt_language)
                            fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files, original_prompt_language)
                            if fixing_result == "Execution stopped by user":
                                return "Execution stopped by user"
                            retry_count += 1
                    else:
                        if is_localhost_command == "1" or is_localhost_command == 1 or is_localhost_command == None:
                            logger.info(
                                f"#### `Command agent` believes this is localhost `{step['command']}`. "
                                "It has run successfully, so there is potentially no error. "
                                "However, I have already shut it down. We can open it separately in your terminal."
                            )

                            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                            user_run = input()

                            user_select_run, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                            user_select_run = user_select_run.lower()
                            if user_select_run == 'a':
                                bash_commands.append(step['command'])
                                self.open_terminal(bash_commands)
                            break
                        else:
                            bash_commands.append(step['command'])
                            break
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['prompt'], file_name)
                        logger.info(f" #### `FileUpdater` has successfully updated {file_name}")
                    else:
                        logger.debug("\n #### `FileUpdater`: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"  `StepExecutor` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"  `StepExecutor`: Step failed after {self.max_retry_attempts} attempts: {step['prompt']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"
                fixing_steps = await self.get_error_planner_requests(
                    error_message, step['prompt'], self.repo.return_os(), compile_files, original_prompt_language)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                if fixing_result == "Execution stopped by user":
                    logger.info(" #### `UserInteractionHandler`: User chose to exit during fixing steps. Skipping current step.")
                    continue
                return f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"

            logger.info(" #### `StepExecutor`: Step completed. Proceeding to the next step.")

        logger.info(" #### `StepExecutor`: All steps have been completed successfully")
        return "All steps completed successfully"

    async def execute_fixing_steps(self, steps_json, compile_files, code_files, original_prompt_language):
        """
        Executes a series of steps provided in JSON format to fix dependency issues.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:

            if step['method'] == 'bash':
                logger.info(f" #### `Compile Command Runner`: {step['error_resolution']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f" #### `Compile Command Runner`:")
                logger.info(f"```yaml\n{step['error_resolution']}\n```")

            logger.info("")
            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
            user_permission = input()

            user_prompt, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
            user_prompt = user_prompt.lower()

            if user_prompt == 'exit':
                logger.info(" #### The user has chosen to exit. The `CommandRunner` is halting execution.")
                return "Execution stopped by user"
            elif user_prompt == 's':
                logger.info(" #### The user has chosen to skip this step.")
                continue

            logger.info(f" #### `FixingStepExecutor`: Executing step: {step['error_resolution']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'], "0")

                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = ','.join(command_output)
                        logger.error(f"  `CommandExecutor` failed with return code {return_code}: {error_message}")

                        ## Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f" #### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                            user_choice = input()

                            user_select, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                            user_select = user_select.lower()
                            
                            if user_select == 'a':
                                logger.info(f" #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command, "0") 
                                if return_code == 0:
                                    break  # Command executed successfully
                                else:
                                    # Update error_message with new command output
                                    error_message = ','.join(command_output)
                                    logger.error(
                                        f"\n #### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                            elif user_select == 'exit':
                                logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                            else:
                                logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")

                        error_check = await self.errorDetection.get_task_plan(error_message)
                        error_type = error_check.get('error_type', 1)
                        AI_error_message = error_check.get('error_message', "")

                        if error_type == 3:
                            logger.info("#### I apologize, but I'm having trouble understanding the issue. This could be due to missing context or unclear dependencies. Let me help you narrow it down:")
                            logger.info("##### 1. Select `Dependency Issue` if you suspect missing or incompatible dependencies")
                            logger.info("##### 2. Select `Code Logic Error` if you think there's a problem with the code implementation")
                            logger.info("##### 3. Select `Exit` if you'd prefer to skip this error\n")
                            logger.info("#### Please choose an option so I can better assist you with resolving this error. If you're unsure, option 1 is a good place to start.\n")
                    

                            logger.info("### Agent is confused due to lack of context. Please select 'Dependency Issue', 'Code Logic Error', or 'Exit' to help me better assist you: ")

                            user_prompt_json1 = input()
                            user_prompt1, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_prompt_json1)
                            user_prompt1 = user_prompt1.lower()

                            if user_prompt1 == "sy":
                                await self.print_code_error(AI_error_message, code_files)
                                retry_count += 1
                                continue  # Re-run the command after fixing the code error
                            elif user_prompt == "de":
                                # Proceed to handle the error
                                fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files, original_prompt_language)
                                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files, original_prompt_language)
                                if fixing_result == "Execution stopped by user":
                                    return "Execution stopped by user"
                                retry_count += 1
                            elif user_prompt == "exit":
                                logger.info(" #### User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                        elif error_type == 1:
                            await self.print_code_error(AI_error_message, code_files)
                            retry_count += 1
                            continue  # Re-run the command after fixing the code error
                        elif error_type == 2:
                             # Proceed to handle the error
                            fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files, original_prompt_language)
                            fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files, original_prompt_language)
                            if fixing_result == "Execution stopped by user":
                                return "Execution stopped by user"
                            retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['error_resolution'], file_name)
                        logger.info(f" #### `FileUpdater` has successfully updated {file_name}")
                    else:
                        logger.debug("\n #### `FileUpdater`: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"  `FixingStepExecutor` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"  `FixingStepExecutor`: Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"
                fixing_steps = await self.get_error_planner_requests(
                    error_message, step['error_resolution'], self.repo.return_os(), compile_files, original_prompt_language)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                if fixing_result == "Execution stopped by user":
                    return "Execution stopped by user"
                return f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"

            logger.info(" #### `FixingStepExecutor`: Step completed. Proceeding to the next step.")

        logger.info(" #### `FixingStepExecutor`: All fixing steps have been completed successfully")
        return "All fixing steps completed successfully"

    async def get_file_planning(self, idea_plan):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def process_creation(self, data):
        moving_processes = data.get('Moving_files', [])
        
        if data.get('Is_creating'):
            new_files = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(new_files)
            
        if moving_processes:
            await self.project.execute_files_creation(moving_processes)
        
        if not data.get('Is_creating') and not moving_processes:
            logger.info(" #### `FileCreationManager`: No new files need to be added or moved at this time.")
