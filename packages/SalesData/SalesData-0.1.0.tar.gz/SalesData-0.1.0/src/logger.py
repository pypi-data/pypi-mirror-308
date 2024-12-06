import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Dict


class Logger:
    """
    Handles logging setup for the application.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.logger = self.get_logger()

    # def get_logger(self, logging_level: str = "INFO") -> logging.Logger:
    def get_logger(self, log_level: str = "INFO") -> logging.Logger:
        """
        Function to create and return common logger to be used for the application
            @return: logger (logging.Logger): Created logger is returned
        """

        # Configure logger
        logging_format = (
            "%(asctime)s.%(msecs)03d: %(name)s: %(levelname)-10s: %(message)s"
        )
        logging.basicConfig(format=logging_format, datefmt="%Y-%m-%d %H:%M:%S")

        # Create a logger
        logger = logging.getLogger(self.app_name)
        log_level = logging.getLevelName(log_level.upper())
        logger.setLevel(log_level)

        # Configure log file handler
        # Logs will be written to log file
        log_dir = "logs/"
        os.makedirs(log_dir, exist_ok=True)

        file_date = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file_name = f"{self.app_name}_{file_date}.log"

        log_file = f"{log_dir}{log_file_name}"

        # Set up rotating file handler
        # Allows the log file to rotate after it reaches a specified size (5 MB here), with up to 3 backups.
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setLevel(log_level)
        # Create a formatter and add it to the rotating file handler
        formatter = logging.Formatter(logging_format, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        return logger

    def log_message(self, logging_level: str, message: str) -> None:
        """
        Function to log messages
            @Param: logging_level (str): Logging level with which message should be logged.
            Below are Valid values for this field
                DEBUG
                INFO
                WARNING
                ERROR
                CRITICAL
            @Param: message (str): Message to be logged
            @Param: custom_fields (dict):
            @return: None
        """

        self.logger.log(logging.getLevelName(logging_level.upper()), message)

    def clear_handlers(self) -> None:
        """
        Function to clear log handlers
            @Param: environment_name : Name of the environment
            @return: None
        """
        # Clear logger handlers

        for handler in self.logger.handlers:
            handler.flush()

        self.logger.handlers.clear()
        logging.shutdown()
