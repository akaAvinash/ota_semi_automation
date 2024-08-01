import time
import os
import pytest
from ota_framework.core.wifi import WiFi
from ota_framework.core.registration import Registration
from ota_framework.core.flags import Flags
from ota_framework.core.ota import OTA
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.device_actions import DeviceActions
from ota_framework.config.constants import *

logger = CustomLogger('OTA_precondition')

class Precon:

    def __init__(self, logs_dir):
        self.wifi = WiFi()
        self.register = Registration()
        self.flags = Flags()
        # Initialize DeviceActions with logs_dir
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        self.device = DeviceActions(logs_dir=logs_dir)

    def wifi_setup(self):
        logger.info("Starting Wi-Fi connection")
        result = self.wifi.connect(ssid=WiFiConstants.SSID, password=WiFiConstants.PASSWORD)
        assert result['success'], f"Wi-Fi connection failed with error: {result.get('error', 'Unknown error')}"
        
        logger.info("Starting Wi-Fi validation")
        validation_result = self.wifi.validate_connection(ssid=WiFiConstants.SSID)
        assert validation_result['success'], f"Wi-Fi validation failed with error: {validation_result.get('error', 'Unknown error')}"
        
        logger.info("Wi-Fi validation passed, Wi-Fi connected")

    def reg_device(self):
        logger.info("Starting device registration")
        registration_result = self.register.register_device(
            username=RegistrationConstants.USERNAME,
            password=RegistrationConstants.PASSWORD
        )
        assert registration_result['success'], f"Device registration failed with error: {registration_result.get('error', 'Unknown error')}"
        logger.info("Device registration successful")        
        validation_result = self.register.validate_registration(username=RegistrationConstants.USERNAME)        
        assert validation_result['success'], f"Device registration validation failed with error: {validation_result.get('error', 'Unknown error')}"
        logger.info("Device registration validation successful")


    def soft_version(self):
        version = self.device.check_software_version()
        logger.info(f"Initial Software Version: {version}")

    def flag(self):
        self.flags.set_flag_0()
        time.sleep(60)
        logger.info("Flag set to 0")

    def flag_440(self):
        self.flags.set_flag_440()
        time.sleep(60)
        logger.info("Flag set to 440")

    def push_app(self):
        self.device.push_and_install_app(app_name='settings_app')
        time.sleep(3)
        
    def boot_utility(self):
        self.device.verify_and_get_boot_utility_slots()
        
    def screen_shooter(self):
        self.device.take_screenshot(filename="filename.png")
        
    def skip_oobe(self):
        self.device.check_and_complete_oobe_based_on_profile()
    
    def alexa(self):
        self.device.enable_alexa()
        
    def config_setup_for_mm_device(self):
        self.device.push_debug_service_file()
        
def main():
    pre = Precon()
    try:
        logger.info("Starting precondition setup.")
        # pre.wifi_setup()
        pre.reg_device()
        logger.info("Precondition setup completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during precondition setup: {e}")

if __name__ == "__main__":
    main()
