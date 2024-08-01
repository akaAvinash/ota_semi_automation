import os
import time
import pytest
from ota_framework.core.ota import OTA
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.test_config import TestConfig

# Initialize the logger
logger = CustomLogger('n_to_u_ota', log_file_name='test_n_to_u.log')

def test_n_to_u_ota():
    try:
        logger.info('Starting n_to_u_ota test')
        
        # Initialize components using TestConfig
        config = TestConfig()
        flash, ota, setup, device, pre = config.get_components()
        
        build_name = "n_to_u"
        
        # Create OTA instance with test_case_name
        ota = OTA(delay=5, test_case_name='test_n_to_u')
        
        # Flash build
        logger.info("Starting build flash.")
        flash.flash_build(build_name)
        logger.info("Waiting for device to be ready.")
        time.sleep(30)
        
        # Perform device setup prior to OTA
        setup.perform_setup()
        
        # Start OTA process
        logger.info("Starting OTA process.")
        ota.start_ota_process()
        logger.info("Waiting for OTA to download & install")
        
        # Perform post OTA actions
        logger.info("Performing post OTA actions.")
        setup.post_ota_actions()
        
        logger.info('n_to_u_ota test completed successfully')

    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        raise
