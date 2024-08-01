from ota_framework.core.shell import Shell
from ota_framework.config.constants import DeviceCommands
from ota_framework.core.custom_logger import CustomLogger

# Initialize the logger for this module
logger = CustomLogger('FlagsLogger')

class Flags:
    @staticmethod
    @logger.log_decorator(level='info')
    def set_flag_0():
        """
        Set the device flag to 0, reboot, and validate.
        
        Returns:
        - dict: A dictionary with 'success', 'output', and 'error' keys.
        """
        # Set the flag to 0
        result = Shell.execute_command(DeviceCommands.FLAG_0)
        if not result['success']:
            logger.error(f"Failed to set flag 0: {result['error']}")
            return result
        
        # Reboot the device
        reboot_result = Shell.execute_command(DeviceCommands.REBOOT)
        if not reboot_result['success']:
            logger.error(f"Failed to reboot device: {reboot_result['error']}")
            return reboot_result
        
        # Validate the flag setting
        return Flags.validate_flag_0()

    @staticmethod
    @logger.log_decorator(level='info')
    def set_flag_440():
        """
        Set the device flag to 0x440, reboot, and validate.
        
        Returns:
        - dict: A dictionary with 'success', 'output', and 'error' keys.
        """
        # Set the flag to 0x440
        result = Shell.execute_command(DeviceCommands.FLAG_440)
        if not result['success']:
            logger.error(f"Failed to set flag 440: {result['error']}")
            return result
        
        # Reboot the device
        reboot_result = Shell.execute_command(DeviceCommands.REBOOT)
        if not reboot_result['success']:
            logger.error(f"Failed to reboot device: {reboot_result['error']}")
            return reboot_result
        
        # Validate the flag setting
        return Flags.validate_flag_440()

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_flag_0():
        """
        Validate if the device flag is set to 0.
        
        Returns:
        - dict: A dictionary with 'success', 'output', and 'error' keys.
        """
        validate_command = DeviceCommands.FLAG_CHECK
        validation_result = Shell.execute_command(validate_command)
        if 'dev_flags: 0' in validation_result['output']:
            validation_result['success'] = True
            validation_result['error'] = None
        else:
            validation_result['success'] = False
            validation_result['error'] = f'Expected dev_flags: 0, but got: {validation_result["output"]}'
        return validation_result

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_flag_440():
        """
        Validate if the device flag is set to 0x440.
        
        Returns:
        - dict: A dictionary with 'success', 'output', and 'error' keys.
        """
        validate_command = DeviceCommands.FLAG_CHECK
        validation_result = Shell.execute_command(validate_command)
        if 'dev_flags: 0x440' in validation_result['output']:
            validation_result['success'] = True
            validation_result['error'] = None
        else:
            validation_result['success'] = False
            validation_result['error'] = f'Expected dev_flags: 0x440, but got: {validation_result["output"]}'
        return validation_result