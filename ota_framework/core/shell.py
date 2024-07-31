import subprocess

class Shell:
    @staticmethod
    def execute_command(command, redirect_output=False, output_file=None):
        """
        Execute a shell command.
        :param command: Command to be executed.
        :param redirect_output: Flag to indicate if output should be redirected.
        :param output_file: File to which output should be redirected.
        :return: A dictionary with 'success', 'output', and 'error' keys, or a process object if redirecting.
        """
        try:
            if redirect_output and output_file:
                file = open(output_file, 'a')
                process = subprocess.Popen(command, shell=True, stdout=file, stderr=file)
                return process
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                success = process.returncode == 0
                return {
                    'success': success,
                    'output': output.decode(),
                    'error': error.decode()
                }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
