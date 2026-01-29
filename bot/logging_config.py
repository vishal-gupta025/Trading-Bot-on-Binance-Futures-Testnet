"""
Logging configuration
"""

import logging
import os
from datetime import datetime


def setup_logging(log_dir: str = "logs"):
    """Setup logging to file and console."""
    
    # Create logs directory
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    # File handler
    log_file = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d_%H-%M-%S}_trading.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
