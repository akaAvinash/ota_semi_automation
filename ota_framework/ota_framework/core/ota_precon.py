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

    def __init__(self):
        self.wifi = WiFi()
        self.register = Registration()
        self.flags = Flags()
        # Initialize DeviceActions with logs_dir
        logs_dir = '/home/ANT.AMAZON.COM/avinaks/Downloads/Playground/ota_framework/logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        self.device = DeviceActions(logs_dir=logs_dir)

    def wifi_setup(self):
        self.wifi.connect(ssid=WiFiConstants.SSID,password=WiFiConstants.PASSWORD)
        logger.info("Starting Wi-Fi connection")
        assert self.wifi.validate_connection(ssid=WiFiConstants.SSID), "Wi-Fi connection failed."
        logger.info("Wi-Fi validation passed, Wi-Fi connected")

    def reg_device(self):
        self.register.register_device(username=RegistrationConstants.USERNAME,password=RegistrationConstants.PASSWORD)
        logger.info("Starting device registration")
        assert self.register.validate_registration(username=RegistrationConstants.USERNAME), "Device registration failed."
        logger.info("Device registration successful")

    def soft_version(self):
        version = self.device.check_software_version()
        logger.info(f"Initial Software Version: {version}")

    def flag(self):
        self.flags.set_flag_0()
        time.sleep(30)
        logger.info("Flag set to 0")

    def flag_440(self):
        self.flags.set_flag_440()
        time.sleep(30)
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