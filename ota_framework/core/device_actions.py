import time
import os
import re
import configparser
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.flags import Flags
from ota_framework.config.constants import SystemCommands, DeviceCommands, OOBECommands, Profiles
from ota_framework.core.shell import Shell

logger = CustomLogger('DeviceLog')

class DeviceActions:
    def __init__(self,logs_dir):
        self.shell = Shell()
        self.max_retries = 5
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '../config/config.ini')
        self.config.read(config_path)
        self.logs_dir = logs_dir
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        self.flag = Flags()

    @logger.log_decorator(level='info')
    def reboot_device(self):
        """
        Reboot the device using the command from DeviceCommands.
        """
        command = DeviceCommands.REBOOT
        self.shell.execute_command(command)

    @logger.log_decorator(level='info')
    def take_screenshot(self, filename='filename.png'):
        """
        Take a screenshot on the device and save it to the logs folder.

        Args:
        - filename (str): Name of the screenshot file.

        Returns:
        - str: Path to the saved screenshot file.
        """
        try:
            # Execute the screenshot command
            command = DeviceCommands.SCREENSHOT_COMMAND
            result = self.shell.execute_command(command)
            logger.info(f"Screenshot command executed: {result}")

            # Pull the screenshot to the local folder
            pull_command = DeviceCommands.PULL_SCREENSHOT
            screenshot_file = os.path.join(self.logs_dir, filename)
            pull_command_with_path = f"{pull_command} /tmp/{filename} {screenshot_file}"
            pull_result = self.shell.execute_command(pull_command_with_path)
            logger.info(f"Pull command executed: {pull_result}")

            if not os.path.isfile(screenshot_file):
                raise FileNotFoundError(f"Screenshot file not found at: {screenshot_file}")

            logger.info(f"Screenshot saved successfully to: {screenshot_file}")

            # Return the path to the saved screenshot
            return screenshot_file
        except Exception as e:
            logger.error(f"Error taking or saving screenshot: {e}")
            raise


    @logger.log_decorator(level='info')
    def check_device_online(self):
        """
        Check if the device is online by running the adb devices command.
        
        Returns:
        - bool: True if the device is online, False otherwise.
        """
        retries = 5
        for attempt in range(retries):
            try:
                result = self.shell.execute_command("adb devices")
                if result['success']:
                    output_lines = result['output'].splitlines()
                    for line in output_lines:
                        if "device" in line and not line.startswith("List of devices attached"):
                            logger.info(f"Device found: {line}")
                            return True
                else:
                    logger.error(f"Error checking device status: {result['error']}")
            except Exception as e:
                logger.error(f"Error checking device status: {e}")

            logger.warning("Device not found, retrying...")
            time.sleep(1)
        
        logger.warning("Device could not be detected after retries.")
        return False
    
    @logger.log_decorator(level='info')
    def check_software_version(self):
        """
        Check the software version of the device.

        Returns:
        - str: Software version.

        Raises:
        - Exception: If there is an error executing the command or parsing the output.
        """
        try:
            command = SystemCommands.SHOW_OS_RELEASE
            result = self.shell.execute_command(command)
            if result['success']:
                logger.info(f"Software version check output: {result['output']}")
                # Extract the software version from the output
                version_match = re.search(r"'com.amazon.devconf/system/device-info/software-version'\s*=\s*'(\d+)'", result['output'])
                if version_match:
                    version = version_match.group(1)
                    return version
                else:
                    raise Exception("Software version not found in the output.")
            else:
                raise Exception(f"Command execution failed: {result['error']}")
        except Exception as e:
            logger.error(f"Error checking software version: {e}")
            raise
        
    @logger.log_decorator(level='info')
    def get_software_version(self):
        """
        Retrieve the software version of the device.

        Returns:
        - str: Software version.

        Raises:
        - Exception: If there is an error executing the command or parsing the output.
        """
        try:
            # Define the command to check the software version
            command = SystemCommands.SHOW_OS_RELEASE
            
            # Execute the command
            result = self.shell.execute_command(command)
            
            # Check if the command was successful
            if result['success']:
                logger.info(f"Software version check output: {result['output']}")
                
                # Extract the software version from the output
                version_match = re.search(r"'com.amazon.devconf/system/device-info/software-version'\s*=\s*'(\d+)'", result['output'])
                
                if version_match:
                    # Return the software version
                    version = version_match.group(1)
                    return version
                else:
                    raise Exception("Software version not found in the output.")
            else:
                raise Exception(f"Command execution failed: {result['error']}")
        except Exception as e:
            logger.error(f"Error getting software version: {e}")
            raise
            
        
    @logger.log_decorator(level='info')
    def enable_alexa(self):
        """
        Enable Alexa on the device using the command from SystemCommands.

        Returns:
        - bool: True if Alexa was successfully enabled, False otherwise.

        Raises:
        - Exception: If there is an error executing the command or parsing the output.
        """
        try:
            command = SystemCommands.ENABLE_ALEXA
            result = self.shell.execute_command(command)
            if result['success']:
                logger.info(f"Enable Alexa command output: {result['output']}")
                # Check if the output indicates success
                if "successfully set to 'true'" in result['output']:
                    return True
                else:
                    raise Exception("Failed to enable Alexa.")
            else:
                raise Exception(f"Command execution failed: {result['error']}")
        except Exception as e:
            logger.error(f"Error enabling Alexa: {e}")
            raise
        
    @logger.log_decorator(level='info')
    def skip_oobe(self):
        """
        Complete the Out-of-Box Experience (OOBE) by executing commands from OOBECommands class.
        Adds a delay of 2 seconds between each command execution.

        Returns:
        - bool: True if OOBE was successfully completed, False otherwise.

        Raises:
        - Exception: If there is an error executing any of the OOBE commands.
        """
        try:
            # List of OOBE commands to execute
            oobe_commands = [
                OOBECommands.USER_SETUP_COMPLETE,
                OOBECommands.DCS_CONFIG,
                OOBECommands.HOME_SCREEN
            ]

            for command in oobe_commands:
                result = self.shell.execute_command(command)
                logger.info(f"Executed command '{command}'. Output: {result['output']}")
                time.sleep(2)

                if not result['success']:
                    raise Exception(f"Command '{command}' failed with error: {result['error']}")

            logger.info("OOBE completed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error completing OOBE: {e}")
            raise
        
    @logger.log_decorator(level='info')
    def verify_and_get_boot_utility_slots(self):
        """
        Verify the status of boot utility slots _a and _b.

        Returns:
        - tuple: Status of slots _a and _b (STATUS_OF_SLOT_a, STATUS_OF_SLOT_b).

        Raises:
        - AssertionError: If the status of any slot does not match the expected values.
        """
        def verify_boot_utility_slots(slot_name):
            command = DeviceCommands.BOOT_CONTROL
            result = self.shell.execute_command(command)
            lines = result['output'].strip().split('\n')
            headers = lines[0].split()
            data = [line.split() for line in lines[1:]]
            for row in data:
                if row[0] == slot_name:
                    return row[3]

        STATUS_OF_SLOT_a = verify_boot_utility_slots('_a')
        STATUS_OF_SLOT_b = verify_boot_utility_slots('_b')

        assert STATUS_OF_SLOT_a == "No", f"Expected 'No' for slot '_a', but got '{STATUS_OF_SLOT_a}'"
        assert STATUS_OF_SLOT_b == "Yes", f"Expected 'Yes' for slot '_b', but got '{STATUS_OF_SLOT_b}'"

        return STATUS_OF_SLOT_a, STATUS_OF_SLOT_b
    
    @logger.log_decorator(level='info')
    def push_and_install_app(self, app_name):
        """
        Push and install an app on the device.

        Args:
        - app_name (str): The name of the app as specified in the config.ini file.
        """
        try:
            app_path = self.config.get('apps', app_name)
            if not app_path or not os.path.exists(app_path):
                logger.error(f"App path for {app_name} is invalid or does not exist.")
                return

            # Push the app to the device
            push_command = f"adb push {app_path} /data/{os.path.basename(app_path)}"
            result = self.shell.execute_command(push_command)
            if not result['success']:
                logger.error(f"Failed to push {app_name} to device: {result['error']}")
                return

            # Install the app on the device
            install_command = f"adb shell vpm install /data/{os.path.basename(app_path)}"
            result = self.shell.execute_command(install_command)
            if result['success']:
                logger.info(f"App {app_name} installed successfully.")
            else:
                logger.error(f"Failed to install {app_name} on device: {result['error']}")
        except Exception as e:
            logger.error(f"Error pushing or installing app {app_name}: {e}")
            raise
        
    @logger.log_decorator(level='info')
    def get_device_name(self):
        """
        Get the product name of the device using the command from SystemCommands.

        Returns:
        - str: Product name of the device.
        """
        try:
            command = SystemCommands.DEVICE_NAME
            result = self.shell.execute_command(command)
            if result['success']:
                # Parse the output to find PRODUCT_NAME
                output_lines = result['output'].splitlines()
                for line in output_lines:
                    if line.startswith("PRODUCT_NAME"):
                        product_name = line.split('=')[1].strip()
                        logger.info(f"Device product name: {product_name}")
                        return product_name
                raise Exception("Product name not found in command output.")
            else:
                raise Exception(f"Command execution failed: {result['error']}")
        except Exception as e:
            logger.error(f"Error getting device name: {e}")
            raise
        
    @logger.log_decorator(level='info')
    def check_and_complete_oobe_based_on_profile(self):
        """
        Check the device profile and complete OOBE if the profile is MULTIMODAL.

        Returns:
        - bool: True if OOBE was completed or no action needed, False if an error occurred.
        """
        try:
            profile = self.get_device_profile()
            if profile == Profiles.TV:
                logger.info("TV profile detected. No action needed.")
                return True
            elif profile in Profiles.MULTIMODAL:
                logger.info(f"MULTIMODAL profile detected. Initiating OOBE completion.")
                if not self.skip_oobe():
                    return False
                self.reboot_device()
                logger.info("Rebooting device. Waiting for 60 seconds for device to come online...")
                time.sleep(60)  
                if self.check_device_online():
                    logger.info("Device rebooted and online.")
                    return True
                else:
                    logger.error("Device did not come online after reboot.")
                    return False
            else:
                logger.warning(f"Unknown profile '{profile}'. No action taken.")
                return False
        except Exception as e:
            logger.error(f"Error checking and completing OOBE based on profile: {e}")
            return False

    @logger.log_decorator(level='info')
    def get_device_profile(self):
        """
        Get the device profile from the Profiles class.

        Returns:
        - str: Device profile (TV or specific MULTIMODAL device name).
        """
        try:
            device_name = self.get_device_name()
            
            if device_name == Profiles.TV:
                return Profiles.TV
            
            # Check if the device_name is in MULTIMODAL and return it
            if device_name in Profiles.MULTIMODAL:
                return device_name
            
            # If device_name is not found in the known profiles
            raise Exception("Unknown device profile.")
        
        except Exception as e:
            logger.error(f"Error getting device profile: {e}")
            raise


    @logger.log_decorator(level='info')
    def push_debug_service_file(self):
        """
        Push the debug files and service config file, to enable app installation.
        """
        try:
            
            # Define the full paths for the files to push
            debug_folder_path = os.path.join(os.path.dirname(__file__), '../config/debug/')
            service_config_path = os.path.join(os.path.dirname(__file__), '../config/service-configuration.conf')
            
            # Define the ADB commands to push files
            debug_command = f"adb push {debug_folder_path} /etc/pkgmgrd/certs/"
            service_config_command = f"adb push {service_config_path} /etc/pkgmgrd/"

            # Execute the command to push the debug folder
            debug_result = self.shell.execute_command(debug_command)
            if debug_result['success']:
                logger.info("Successfully pushed debug files.")
            else:
                logger.error(f"Failed to push debug files: {debug_result['error']}")
                raise Exception("Error occurred while pushing debug files.")

            # Execute the command to push the service configuration file
            service_config_result = self.shell.execute_command(service_config_command)
            if service_config_result['success']:
                logger.info("Successfully pushed service configuration file.")
            else:
                logger.error(f"Failed to push service configuration file: {service_config_result['error']}")
                raise Exception("Error occurred while pushing service configuration file.")

        except Exception as e:
            logger.error(f"Error pushing debug files and service config: {e}")
            raise



if __name__ == "__main__":
    logs_dir = '/home/ANT.AMAZON.COM/avinaks/Downloads/Playground/ota_framework/logs/'
    device_actions = DeviceActions(logs_dir)
    try:
#         device_actions.reboot_device()

        # # Example to take a screenshot
        # screenshot_filename = "filename.png"
        # screenshot_path = device_actions.take_screenshot(screenshot_filename)
        # print(f"Screenshot saved to: {screenshot_path}")

#         # Example to check device online status
#         is_online = device_actions.check_device_online()
#         print(f"Device online: {is_online}")

#         # Example to get software version
        # software_version = device_actions.get_software_version()
        # print(f"Software version: {software_version}")
        
        # get_soft = device_actions.get_software_version()
        # print(f"Soft version: {get_soft}")

#         # Example to enable Alexa
#         device_actions.enable_alexa()

#         # Example to complete OOBE
#         device_actions.complete_oobe()

#         # Example to push and install an app
#         device_actions.push_and_install_app('settings_app')
#         device_actions.push_and_install_app('carousel_app')
#         device_actions.get_device_name()
          device_actions.get_device_name()
          device_actions.get_device_profile()
          device_actions.check_and_complete_oobe_based_on_profile()
        # device_actions.verify_and_get_boot_utility_slots()
        # device_actions.push_debug_service_file()
          
    except Exception as e:
        print(f"Error: {e}")