import logging
import os
from functools import wraps

class CustomLogger:
    def __init__(self, name, log_file_name='project.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Ensure the logs directory exists
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, log_file_name)

        # File handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def log_decorator(self, level='info'):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if level == 'info':
                    self.info(f"Calling {func.__name__}")
                elif level == 'debug':
                    self.debug(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
                elif level == 'warning':
                    self.warning(f"Warning in {func.__name__}: {args}")
                try:
                    result = func(*args, **kwargs)
                    if level == 'info':
                        self.info(f"{func.__name__} returned {result}")
                    elif level == 'debug':
                        self.debug(f"{func.__name__} returned {result}")
                    return result
                except Exception as e:
                    self.error(f"Exception in {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator
