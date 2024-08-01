# import subprocess

# class Shell:
#     @staticmethod
#     def execute_command(command, redirect_output=False, output_file=None):
#         """
#         Execute a shell command.
#         :param command: Command to be executed.
#         :param redirect_output: Flag to indicate if output should be redirected.
#         :param output_file: File to which output should be redirected.
#         :return: A dictionary with 'success', 'output', and 'error' keys, or a process object if redirecting.
#         """
#         try:
#             if redirect_output and output_file:
#                 file = open(output_file, 'a')
#                 process = subprocess.Popen(command, shell=True, stdout=file, stderr=file)
#                 return process
#             else:
#                 process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                 output, error = process.communicate()
#                 success = process.returncode == 0
#                 return {
#                     'success': success,
#                     'output': output.decode(),
#                     'error': error.decode()
#                 }
#         except Exception as e:
#             return {
#                 'success': False,
#                 'output': '',
#                 'error': str(e)
#             }

import subprocess

class Shell:
    @staticmethod
    def execute_command(command, redirect_output=False, output_file=None):
        """
        Execute a shell command and capture the output.

        :param command: The command to be executed.
        :param redirect_output: Whether to redirect output to a file.
        :param output_file: The file to which the output will be redirected.
        :return: A dictionary with keys 'success', 'output', and 'error'.
        """
        result = {
            'success': False,
            'output': '',
            'error': ''
        }
        
        try:
            if redirect_output and output_file:
                # Open file in write mode
                with open(output_file, 'w') as file:
                    process = subprocess.Popen(command, shell=True, stdout=file, stderr=file)
                    process.wait()
                    result['success'] = process.returncode == 0
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                result['success'] = process.returncode == 0
                result['output'] = stdout.decode('utf-8')
                result['error'] = stderr.decode('utf-8')
            
            # Print command and result
            print(f"Command executed: {command}")
            print(f"Output: {result['output']}")
            print(f"Error: {result['error']}")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"Error executing command: {e}")
        
        return result
