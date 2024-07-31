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
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        # Set the flag to 0
        result = Shell.execute_command(DeviceCommands.FLAG_0)
        if not result['success']:
            return result
        
        # Reboot the device
        reboot_result = Shell.execute_command(DeviceCommands.REBOOT)
        if not reboot_result['success']:
            return reboot_result
        
        # Validate the flag setting
        return Flags.validate_flag_0()

    @staticmethod
    @logger.log_decorator(level='info')
    def set_flag_440():
        """
        Set the device flag to 0x440, reboot, and validate.
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        # Set the flag to 0x440
        result = Shell.execute_command(DeviceCommands.FLAG_440)
        if not result['success']:
            return result
        
        # Reboot the device
        reboot_result = Shell.execute_command(DeviceCommands.REBOOT)
        if not reboot_result['success']:
            return reboot_result
        
        # Validate the flag setting
        return Flags.validate_flag_440()

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_flag_0():
        """
        Validate if the device flag is set to 0.
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        validate_command = DeviceCommands.FLAG_CHECK
        validation_result = Shell.execute_command(validate_command)
        if 'dev_flags: 0' in validation_result['output']:
            validation_result['success'] = True
        else:
            validation_result['success'] = False
            validation_result['error'] = f'Expected dev_flags: 0, but got: {validation_result["output"]}'
        return validation_result

    @staticmethod
    @logger.log_decorator(level='info')
    def validate_flag_440():
        """
        Validate if the device flag is set to 0x440.
        :return: A dictionary with 'success', 'output', and 'error' keys.
        """
        validate_command = DeviceCommands.FLAG_CHECK
        validation_result = Shell.execute_command(validate_command)
        if 'dev_flags: 0x440' in validation_result['output']:
            validation_result['success'] = True
        else:
            validation_result['success'] = False
            validation_result['error'] = f'Expected dev_flags: 0x440, but got: {validation_result["output"]}'
        return validation_result

# # Example usage
# if __name__ == "__main__":
#     flags = Flags()
    
#     # Set flag to 0 and validate
#     result_set_0 = flags.set_flag_0()
#     print(result_set_0)
    
#     # Set flag to 0x440 and validate
#     result_set_440 = flags.set_flag_440()
#     print(result_set_440)
    
#     vali_flag_0 = flags.validate_flag_0()
#     print(vali_flag_0)
