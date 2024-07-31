import time
from ota_framework.config.constants import WiFiCommands
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.shell import Shell

# Initialize the logger for this module
logger = CustomLogger('WiFiLogger')

class WiFi:
    @staticmethod
    @logger.log_decorator(level='info')
    def connect(ssid, password):
        """
        Connect to the WiFi network using the provided SSID and password.
        :param ssid: WiFi SSID
        :param password: WiFi password
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        commands = [
            (WiFiCommands.SCAN, "Scanning for WiFi networks"),
            (WiFiCommands.GET_SCAN_RESULTS, "Getting scan results"),
            (WiFiCommands.ADD_NETWORK.format(ssid=ssid, password=password), "Adding WiFi network"),
            (WiFiCommands.GET_CONFIG, "Getting WiFi configuration"),
            (WiFiCommands.CONNECT_WIFI.format(ssid=ssid), "Connecting to WiFi"),
            (WiFiCommands.SAVE_CONFIG, "Saving WiFi configuration")
        ]
        
        for command, description in commands:
            logger.info(description)
            result = Shell.execute_command(command)
            if not result['success']:
                logger.error(f"Failed at step: {description}")
                return result

        return WiFi.validate_connection(ssid)

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_connection(ssid, retries=5, delay=5):
        """
        Validate if the device is connected to the WiFi network.
        Retry the validation up to `retries` times if it fails.
        :param ssid: WiFi SSID
        :param retries: Number of retry attempts
        :param delay: Delay between retry attempts
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        for attempt in range(1, retries + 1):
            logger.info(f"Validating connection to WiFi SSID: {ssid}, Attempt: {attempt}")
            result = Shell.execute_command(WiFiCommands.VALIDATE)
            if 'networkState: CONNECTED' in result.get('output', ''):
                result['success'] = True
                logger.info(f"Successfully connected to WiFi SSID: {ssid} on attempt {attempt}")
                return result
            else:
                logger.error(f"Validation failed on attempt {attempt}. Retrying after {delay} seconds...")
                time.sleep(delay)
        
        result['success'] = False
        result['error'] = f"Failed to validate connection to WiFi SSID: {ssid} after {retries} attempts. Output: {result.get('output', '')}"
        logger.error(result['error'])
        return result

