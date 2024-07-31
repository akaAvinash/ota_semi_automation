# ota_framework/core/test_config.py
import os
from ota_framework.core.ota import OTA
from ota_framework.core.flash_sequence import DeviceFlasher
from ota_framework.core.ota_precon import Precon
from ota_framework.core.device_actions import DeviceActions
from ota_framework.core.device_setup import DeviceSetup

class TestConfig:
    def __init__(self):
        self.logs_dir = '/home/ANT.AMAZON.COM/avinaks/Downloads/Playground/ota_framework/logs'
        
        # Ensure the logs directory exists
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        self.pre = Precon()
        self.flash = DeviceFlasher()
        self.ota = OTA()
        self.device = DeviceActions(logs_dir=self.logs_dir)
        self.setup = DeviceSetup(self.pre, logs_dir=self.logs_dir)

    def get_components(self):
        return self.flash, self.ota, self.setup, self.device
