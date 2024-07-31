import os
import time
import pytest
from ota_framework.core.custom_logger import CustomLogger
from ota_framework.core.test_config import TestConfig 

# Initialize the logger
logger = CustomLogger('n_1_to_n_ota', log_file_name='test_n_1_to_n.log')

# Mark the test to repeat 10 times
@pytest.mark.skipif(os.getenv('DISABLE_N_1_TO_N_OTA') == '1', reason="Test case is active")
def test_n_1_to_n_ota():
    logger.info(f"DISABLE_N_1_TO_N_OTA value: {os.getenv('DISABLE_N_1_TO_N_OTA')}")
    try:
        logger.info('Starting n_1_to_n_ota test')
        
        # Initialize components using TestConfig
        config = TestConfig()
        flash, ota, setup, device = config.get_components()
        
        build_name = "n_1_to_n"
        
        # # Flash build
        # logger.info("Starting build flash.")
        # flash.flash_build(build_name)
        # time.sleep(200)
        
        # Perform device setup prior to OTA
        # setup.perform_setup()
        
        # # Start OTA process
        # logger.info("Starting OTA process.")
        # ota.start_ota_process()
        # logger.info("Waiting for OTA to download & install")
        # time.sleep(9 * 60)
        
        # Perform post OTA actions
        logger.info("Performing post OTA actions.")
        setup.post_ota_actions()
        
        logger.info('n_1_to_n_ota test completed successfully')

    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        raise
