# src/utils/logger.py

import os
import logging
import logging.handlers

def setup_logger():
    """
    Set up the logger for the AI Agent Framework.

    Environment variables:
      - LOG_DESTINATION: Set to "syslog" to send logs to syslog; defaults to "file".
      - LOG_FILE: The file path to use when logging to a file; defaults to "ai_agent.log".

    Returns:
        A configured logger instance.
    """
    # Determine the log destination; default to "file"
    log_destination = os.environ.get("LOG_DESTINATION", "file").lower()

    # Create a logger for the framework
    logger = logging.getLogger("infrastructure")
    logger.setLevel(logging.DEBUG)  # Set desired logging level

    # Remove any pre-existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define a formatter for consistency in logs
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Setup handler based on log destination
    if log_destination == "syslog":
        try:
            # Attempt to use the local syslog socket (/dev/log) common on Linux systems.
            handler = logging.handlers.SysLogHandler(address='/dev/log')
        except Exception:
            # Fallback to a UDP syslog handler if /dev/log is not available.
            handler = logging.handlers.SysLogHandler(address=('localhost', 514))
    else:
        # Default to logging to a file.
        log_file = os.environ.get("LOG_FILE", "infrastructure.log")
        handler = logging.FileHandler(log_file)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Optionally also log to console for real-time feedback.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger on import if needed.
logger = setup_logger()

if __name__ == "__main__":
    # Example usage: log a test message.
    logger.info("Logger is configured and running.")
