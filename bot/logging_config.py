import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configures the logging system for the trading bot.
    Sets up both a file handler and a console handler.
    """
    # Ensure logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "trading_bot.log")
    
    # Create a custom logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture everything; handlers will filter

    # Create formatters
    # Format: [2025-03-29 14:32:01] [INFO] [orders] - Placing MARKET BUY order for BTCUSDT
    log_format = logging.Formatter(
        '[%(getAsTime)s] [%(levelname)s] [%(module)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Custom formatter class to match the slightly idiosyncratic [TIMESTAMP] request
    # Note: Standard logging.Formatter uses asctime. We'll use a subclass to ensure exact bracket style.
    class CustomFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            return super().formatTime(record, datefmt)

        def format(self, record):
            record.getAsTime = self.formatTime(record, self.datefmt)
            return super().format(record)

    custom_formatter = CustomFormatter(
        '[%(getAsTime)s] [%(levelname)s] [%(module)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(custom_formatter)

    # File Handler
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(custom_formatter)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Initialize and export the logger
logger = setup_logging()
