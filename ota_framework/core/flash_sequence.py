import os
import time
import subprocess
import configparser
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
            
            # Wait for the device to come back online
            self.logger.info("Waiting for device to come back online...")
            self.wait_for_device_ready(timeout=180)  # Wait for 3 minutes
            
        else:
            self.logger.warning(f"Build path for {build_name} is empty or does not exist: {build_path}")

    def is_device_ready(self):
        """
        Check if the device is ready by using the adb devices command and looking for the specific DSN.
        
        Returns:
        - bool: True if the device is listed and ready, False otherwise.
        """
        try:
            # Retrieve the device serial number from the environment variable
            aserial = os.getenv('DEVICE_SERIAL_NUMBER')
            if not aserial:
                self.logger.error("DEVICE_SERIAL_NUMBER environment variable is not set.")
                return False
            
            # Run the adb devices command
            result = subprocess.run(
                ["adb", "devices"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check the output
            output = result.stdout.strip()
            
            if result.returncode != 0:
                self.logger.error(f"adb command failed with error: {result.stderr}")
                return False
            
            # Check if the DSN is in the output and listed as "device"
            for line in output.splitlines():
                if aserial in line and "device" in line:
                    self.logger.info(f"Device {aserial} is listed as ready.")
                    return True
            
            self.logger.info(f"Device {aserial} is not listed or not ready.")
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking device readiness: {e}")
            return False

    def wait_for_device_ready(self, timeout=180):
        """
        Wait for the device to become ready, checking periodically using adb devices.
        
        Parameters:
        - timeout (int): Maximum time to wait for the device to become ready (in seconds).
        
        Raises:
        - TimeoutError: If the device does not become ready within the timeout period.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_device_ready():
                self.logger.info("Device is ready.")
                return True
            self.logger.info("Device not ready yet. Checking again in 10 seconds...")
            time.sleep(10) 
        self.logger.error("Device did not come online in time.")
        raise TimeoutError("Device did not come online in time.")

# Example usage
if __name__ == "__main__":
    build_name = "n_1_to_n"
    
    flasher = DeviceFlasher()
    flasher.flash_build(build_name)
