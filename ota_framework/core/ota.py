import os
import time
import threading
from ota_framework.config.constants import OTACommands
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.shell import Shell

# Initialize the logger for this module
logger = CustomLogger('OTALogger')

class OTA:
    def __init__(self, delay=5, test_case_name='default'):
        self.delay = delay
        self.test_case_name = test_case_name
        self.log_folder = 'logs'
        self.log_file = os.path.join(self.log_folder, f'{test_case_name}_ota_logs.txt')  # File to store OTA logs
        self.log_command = OTACommands.OTA_LOG_COMMAND  # Assuming this is the command for log collection
        
        # Retrieve DSN from environment variables
        self.dsn = os.getenv('DEVICE_SERIAL_NUMBER')
        
        # Ensure the logs directory exists
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        # Validate DSN
        if not self.dsn:
            logger.error("No DEVICE_SERIAL_NUMBER found in environment variables.")
            raise EnvironmentError("DEVICE_SERIAL_NUMBER environment variable not set.")

    def start_log_collection(self):
        """
        Start collecting logs in a separate thread and write to a log file.
        """
        logger.info("Starting log collection.")
        
        def log_collection():
            # Execute the log collection command and redirect output to the log file
            process = Shell.execute_command(self.log_command, redirect_output=True, output_file=self.log_file)
            process.wait()  # Wait for the process to complete

        # Start the log collection thread
        log_thread = threading.Thread(target=log_collection)
        log_thread.daemon = True
        log_thread.start()
        return log_thread

    def start_ota_process(self):
        """
        Start the OTA process by executing defined commands with a delay.
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        # Start log collection in parallel
        log_thread = self.start_log_collection()
        
        # Ensure DSN is used in commands if needed
        commands = [
            OTACommands.FORCE_SYNC_OTA.format(dsn=self.dsn),
            OTACommands.FORCE_UPDATE_OTA.format(dsn=self.dsn),
            OTACommands.START_OTA.format(dsn=self.dsn),
            OTACommands.SHOW_OTA_STATUS.format(dsn=self.dsn),
        ]
        
        results = []

        for command in commands:
            logger.info(f"Executing OTA command: {command}")
            result = Shell.execute_command(command)
            
            if result['success']:
                logger.info(f"Command succeeded: {command}")
            else:
                logger.error(f"Command failed: {command} - Error: {result.get('error', 'No error message provided')}")
            
            results.append(result)
            
            if not result['success']:
                break
            
            time.sleep(self.delay)
        
        # Wait for the OTA process to complete and install
        logger.info("Waiting for 10 minutes for the OTA process to complete and install.")
        time.sleep(600)  # Wait for 10 minutes (600 seconds)

        # Wait for the log collection thread to finish
        log_thread.join(timeout=5)  # Adjust the timeout as needed

        return results

# Example usage
if __name__ == "__main__":
    ota = OTA(delay=5, test_case_name='test_n_1_to_n')
    ota_results = ota.start_ota_process()
    for result in ota_results:
        print(result)
