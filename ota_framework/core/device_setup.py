import time
from ota_framework.core.ota_precon import Precon
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.device_actions import DeviceActions

# Initialize the logger for this module
logger = CustomLogger('DeviceSetupLogger')

class DeviceSetup:
    def __init__(self, precon, logs_dir):
        """
        Initialize the DeviceSetup class with Precon and DeviceActions instances.

        Args:
        - precon (Precon): An instance of the Precon class for device setup.
        - logs_dir (str): Directory path for storing logs.
        """
        self.precon = Precon(logs_dir)
        self.logs_dir = logs_dir
        self.device = DeviceActions(logs_dir=self.logs_dir)
        self.initial_version = None

    def perform_setup(self):
        """
        Perform initial setup tasks including connecting device to Wi-Fi,
        registering the device, checking software version, and setting flags.
        """
        self.precon.wifi_setup()  # Connect device to Wi-Fi
        self.precon.reg_device()  # Register device
        self.initial_version = self.precon.soft_version()  # Store initial software version
        self.precon.config_setup_for_mm_device()  # Push debug files and configure the device
        self.precon.push_app()  # Push and install apps
        self.precon.flag()  # Set device flag before OTA

    def post_ota_actions(self):
        """
        Execute actions required after the OTA update including verifying the update,
        enabling Alexa, configuring the device, taking screenshots, and installing apps.
        """
        # Verify the OTA update using the initial software version
        self.verify_ota_update(self.device.get_software_version, self.initial_version)        
        self.precon.flag_440()  # Set device flag to 440
        self.precon.screen_shooter()  # Take OOBE screenshot
        self.precon.check_app() # To check if apps are present 
        self.precon.skip_oobe()  # Skip OOBE for MM devices
        self.precon.boot_utility()  # Perform boot utility check
        self.precon.alexa()  # Enable Alexa

    def get_initial_software_version(self):
        """
        Retrieve the initial software version before the OTA update.

        Returns:
        - str: Initial software version.
        """
        return self.initial_version
    
    def verify_ota_update(self, get_software_version, initial_version, retries=3):
        """
        Verify if the OTA update was successful by comparing the current software version with the initial one.
        Retries up to a specified number of attempts if the version has not changed.

        Args:
        - get_software_version (callable): Function to get the current software version.
        - initial_version (str): Software version before the OTA update.
        - retries (int): Number of retry attempts (default is 3).

        Raises:
        - AssertionError: If the software version does not change after the specified number of retries.
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
    
