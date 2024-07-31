import time
from ota_framework.core.ota_precon import Precon
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.device_actions import DeviceActions

# Initialize the logger for this module
logger = CustomLogger('DeviceSetupLogger')

class DeviceSetup:
    def __init__(self, precon,logs_dir):
        self.precon = Precon()
        self.logs_dir = logs_dir
        self.device = DeviceActions(logs_dir=self.logs_dir)
        self.initial_version = None

    def perform_setup(self):
        # Connect device to Wi-Fi
        self.precon.wifi_setup()
        
        # Register device
        self.precon.reg_device()
        
        # Check device software version and store it
        self.initial_version = self.precon.soft_version() 
        
        # Set device flag before OTA
        self.precon.flag()

    def post_ota_actions(self):
        # Verify the OTA update using the initial software version
        self.verify_ota_update(self.device.get_software_version, self.initial_version)
        
        # Enabling Alexa
        self.precon.alexa()
        
        # Set device flag to 440
        self.precon.flag_440()
        
        # Push debug files for app installation
        self.precon.config_setup_for_mm_device()
        
        # Take OOBE screen-shot
        self.precon.screen_shooter()
        
        # To skip OOBE in MM devices
        self.precon.skip_oobe()
        
        # Push and install apps
        self.precon.push_app()
        
        # # Boot utility check
        self.precon.boot_utility()

    def get_initial_software_version(self):
        """
        Return the initial software version before the OTA update.
        """
        return self.initial_version
    
    def verify_ota_update(self, get_software_version, initial_version, retries=3):
        """
        Verify if the OTA update was successful by checking the software version.
        Retries up to a specified number of attempts if the version has not changed.
        :param get_software_version: Function to get the current software version.
        :param initial_version: Software version before the OTA update.
        :param retries: Number of retry attempts.
        """
        for attempt in range(retries):
            current_version = get_software_version()
            logger.debug(f"Attempt {attempt + 1}: Software version after OTA: {current_version}")
            if current_version != initial_version:
                logger.info("OTA update successful. Software version changed.")
                return True
            else:
                logger.warning(f"Attempt {attempt + 1}: Software version did not change.")
                if attempt < retries - 1:
                    time.sleep(60)  
        else:
            logger.error(f"OTA update failed. Software version did not change after {retries} attempts: {current_version}")
            assert False, f"OTA update failed. Software version did not change: {current_version}"
