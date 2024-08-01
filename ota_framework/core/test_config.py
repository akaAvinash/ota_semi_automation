# ota_framework/core/test_config.py
import os
from ota_framework.core.ota import OTA
from ota_framework.core.flash_sequence import DeviceFlasher
from ota_framework.core.ota_precon import Precon
from ota_framework.core.device_actions import DeviceActions
from ota_framework.core.device_setup import DeviceSetup

class TestConfig:
    def __init__(self):
        self.logs_dir = os.path.join(os.path.dirname(__file__), '../../logs')
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        self.pre = Precon(self.logs_dir)
        self.flash = DeviceFlasher()
        self.ota = OTA()
        self.device = DeviceActions(logs_dir=self.logs_dir)
        self.setup = DeviceSetup(self.pre, logs_dir=self.logs_dir) 

    def get_components(self):
        return self.flash, self.ota, self.setup, self.device, self.pre