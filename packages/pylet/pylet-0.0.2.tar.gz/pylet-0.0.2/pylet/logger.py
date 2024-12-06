import logging
import sys
from logging.handlers import RotatingFileHandler

# Create a custom logger named 'pylet'
logger = logging.getLogger("pylet")

# Set the default logging level (adjust as needed)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Log all levels to console

file_handler = RotatingFileHandler(
    "pylet.log", maxBytes=5 * 1024 * 1024, backupCount=2
)
file_handler.setLevel(logging.INFO)  # Log INFO and above to file

# Create formatters and add them to the handlers
console_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
)
file_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
