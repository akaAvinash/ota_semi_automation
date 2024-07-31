import os
import configparser
import subprocess
import time
from ota_framework.core.custom_logger import CustomLogger

class DeviceFlasher:
    CONFIG_PATH = "ota_framework/config/config.ini"

    def __init__(self):
        self.logger = CustomLogger('FlashLog')
        self.config = self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(DeviceFlasher.CONFIG_PATH)
            return config
        except configparser.Error as e:
            self.logger.error(f"Failed to load configuration from {DeviceFlasher.CONFIG_PATH}: {e}")
            raise

    def flash_device(self, build_path):
        # Retrieve the device serial number from the environment variable
        aserial = os.getenv('DEVICE_SERIAL_NUMBER')
        fserial = aserial
        
        if not aserial:
            self.logger.error("DEVICE_SERIAL_NUMBER environment variable is not set.")
            raise ValueError("DEVICE_SERIAL_NUMBER environment variable is not set.")
        
        try:
            self.logger.info(f"Executing flash command in directory: {build_path}")
            subprocess.run(
                ["python3", "flashimage.py", f"--aserial={aserial}", f"--fserial={fserial}"],
                cwd=build_path,
                check=True
            )
            self.logger.info("Build flashed successfully")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to flash build in directory {build_path}. Error: {e}")
            raise

    def flash_build(self, build_name):
        build_path = self.config.get("builds", build_name, fallback=None)
        if build_path and os.path.exists(build_path):
            self.logger.info(f"Flashing device with build: {build_path}")
            self.flash_device(build_path)
            
            # Wait for 4 minutes (240 seconds) to allow the device to come back online
            self.logger.info("Waiting for 4 minutes for the device to come back online...")
            time.sleep(240)
            
        else:
            self.logger.warning(f"Build path for {build_name} is empty or does not exist: {build_path}")

if __name__ == "__main__":
    build_name = "n_1_to_n"

    flasher = DeviceFlasher()
    flasher.flash_build(build_name)
