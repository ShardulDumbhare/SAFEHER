"""
Logger Configuration - Centralized logging for the application
"""
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("SAFEHER")
logger.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler (all logs)
file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, f"safeher_{datetime.now().strftime('%Y%m%d')}.log")
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Error file handler (errors only)
error_handler = logging.FileHandler(
    os.path.join(LOG_DIR, "safeher_errors.log")
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

# Console handler (development)
if os.getenv('FLASK_ENV') == 'development':
    try:
        import sys
        import io
        # Fix Windows encoding issues
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Convenience functions
def info(msg):
    logger.info(msg)

def debug(msg):
    logger.debug(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)
