import time
from ota_framework.config.constants import RegistrationCommands, RegistrationConstants
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.shell import Shell

# Initialize the logger for this module
logger = CustomLogger('RegistrationLogger')

class Registration:
    @staticmethod
    @logger.log_decorator(level='info')
    def register_device(username, password):
        """
        Register the device using the provided username and password.
        :param username: Username for registration
        :param password: Password for registration
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        command = RegistrationCommands.REGISTER_DEVICE.format(username=username, password=password)
        
        logger.info(f"Registering device for user: {username}")
        result = Shell.execute_command(command)
        
        if result['success']:
            logger.info("Device registration successful.")
        else:
            logger.error("Failed to register device.")
        
        return result

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_registration(username, retries=5, delay=5):
        """
        Validate if the device registration was successful.
        Retry the validation up to `retries` times if it fails.
        :param username: Username for registration validation
        :param retries: Number of retry attempts
        :param delay: Delay between retry attempts
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        for attempt in range(1, retries + 1):
            logger.info(f"Validating device registration for user: {username}, Attempt: {attempt}")
            result = Shell.execute_command(RegistrationCommands.VALIDATE_REGISTRATION)
            if 'DEVICE_REGISTERED' in result['output']:
                result['success'] = True
                logger.info(f"Device registration validated successfully for user: {username} on attempt {attempt}")
                return result
            else:
                logger.warning(f"Validation failed on attempt {attempt}. Retrying after {delay} seconds...")
                time.sleep(delay)
        
        result['success'] = False
        result['error'] = f"Failed to validate device registration for user: {username} after {retries} attempts. Output: {result['output']}"
        logger.error(result['error'])
        return result
