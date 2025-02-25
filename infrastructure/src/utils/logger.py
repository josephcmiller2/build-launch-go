# src/utils/logger.py

import os
import logging
import logging.handlers

def setup_logger():
    """
    Set up the logger for the AI Agent Framework.

    Environment variables:
      - LOG_LEVEL: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL); defaults to "INFO"
      - LOG_DESTINATION: Set to "syslog" to send logs to syslog; defaults to "file"
      - LOG_FILE: The file path to use when logging to a file; defaults to "infrastructure.log"

    Returns:
        A configured logger instance.
    """
    # Get log level from environment variable, default to INFO
    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Determine the log destination; default to "file"
    log_destination = os.environ.get("LOG_DESTINATION", "file").lower()
    
    # Create a logger for the framework
    logger = logging.getLogger("infrastructure")
    
    # Add debug output to verify configuration
    print(f"Configuring logger with level: {log_level_str} ({log_level})")
    
    # Important: Configure the root logger as well
    logging.basicConfig(level=log_level)
    
    logger.setLevel(log_level)

    # Remove any pre-existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define a formatter for consistency in logs
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Setup handler based on log destination
    if log_destination == "syslog":
        try:
            # Attempt to use the local syslog socket (/dev/log) common on Linux systems
            handler = logging.handlers.SysLogHandler(address='/dev/log')
        except Exception:
            # Fallback to a UDP syslog handler if /dev/log is not available
            handler = logging.handlers.SysLogHandler(address=('localhost', 514))
    else:
        # Default to logging to a file
        log_file = os.environ.get("LOG_FILE", "infrastructure.log")
        handler = logging.FileHandler(log_file)

    handler.setFormatter(formatter)
    handler.setLevel(log_level)  # Also set handler level
    logger.addHandler(handler)

    # Optionally also log to console for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)  # Set console handler level
    logger.addHandler(console_handler)

    # Log the configuration
    logger.info(f"Logger configured with level: {log_level_str}")
    logger.info(f"Log destination: {log_destination}")

    return logger

# Initialize the logger on import
logger = setup_logger()

if __name__ == "__main__":
    # Example usage: log messages at different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
