import os
import time
import threading
from ota_framework.config.constants import OTACommands
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.shell import Shell

# Initialize the logger for this module
logger = CustomLogger('OTALogger')

class OTA:
    def __init__(self, delay=5, test_case_name=None):
        """
        Initialize the OTA class with a delay and test case name.
        
        :param delay: Delay between OTA commands in seconds.
        :param test_case_name: Name of the test case for logging purposes.
        """
        self.delay = delay
        self.test_case_name = test_case_name if test_case_name is not None else 'default'
        self.log_folder = 'logs'
        self.log_file = os.path.join(self.log_folder, f'{self.test_case_name}_ota_logs.txt')
        self.log_command = OTACommands.OTA_LOG_COMMAND
        
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
        :return: The log collection thread.
        """
        logger.info("Starting log collection.")
        
        def log_collection():
            process = Shell.execute_command(self.log_command, redirect_output=True, output_file=self.log_file)
            process.wait()

        log_thread = threading.Thread(target=log_collection)
        log_thread.daemon = True
        log_thread.start()
        return log_thread

    def start_ota_process(self):
        """
        Start the OTA process by executing defined commands with a delay.
        :return: A list of dictionaries with 'success', 'output', and 'error' keys.
        """
        log_thread = self.start_log_collection()

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
        
        # Re-execute the FORCE_UPDATE_OTA command
        force_update_result = Shell.execute_command(OTACommands.FORCE_UPDATE_OTA.format(dsn=self.dsn))
        results.append(force_update_result)
        
        if force_update_result['success']:
            logger.info("Re-execution of FORCE_UPDATE_OTA succeeded.")
        else:
            logger.error(f"Re-execution of FORCE_UPDATE_OTA failed - Error: {force_update_result.get('error', 'No error message provided')}")
        
        # Wait for the OTA process to complete and install
        logger.info("Waiting for 10 minutes for the OTA process to complete and install.")
        time.sleep(600) 

        # Wait for the log collection thread to finish
        log_thread.join(timeout=5)
        return results
    
    def force_sync(self):
        """
        Execute the force sync OTA command twice with a 10-second gap.
        :return: A list of dictionaries with 'success', 'output', and 'error' keys.
        """
        commands = [
            OTACommands.FORCE_SYNC_OTA.format(dsn=self.dsn),
            OTACommands.FORCE_SYNC_OTA.format(dsn=self.dsn)
        ]
        
        results = []

        for command in commands:
            logger.info(f"Executing OTA force sync command: {command}")
            result = Shell.execute_command(command)
            
            if result['success']:
                logger.info(f"Force sync command succeeded: {command}")
            else:
                logger.error(f"Force sync command failed: {command} - Error: {result.get('error', 'No error message provided')}")
            
            results.append(result)
            
            if not result['success']:
                break
            
            time.sleep(10)  # 10-second gap between commands

        return results
