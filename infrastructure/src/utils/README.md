# AI Agent Framework Logger

This repository includes a flexible logging utility that supports both file-based logging and syslog logging. The logger is designed for ease of configuration and use within the AI Agent Framework.

## Overview

The logger is set up in the `utils/logger.py` module. It reads configuration from environment variables:

- **LOG_DESTINATION:**  
  Set to `"syslog"` to log to the system syslog; any other value (or omission) defaults to file logging.
  
- **LOG_FILE:**  
  Specifies the file path to write logs if file logging is used. Defaults to `ai_agent.log` if not provided.

The logger also outputs log messages to the console, which is useful during development.

## Installation

Ensure you have the required dependencies installed (e.g., Python 3 and the `logging` package, which is part of the standard library). Then, clone the repository and set up your environment as needed.

## File Logging (Default)
```
bash
git clone https://your-repository-url.git
cd your-repository
```

## Syslog Logging

```
export LOG_FILE="/path/to/your/logfile.log"
export LOG_DESTINATION="file"
```

## Usage
Import the preconfigured logger from the `utils` package and use it throughout your application.

### Example: Logging to a File
```
# example_file_logging.py
import os
from utils.logger import logger

# Optionally configure environment variables (for demonstration purposes)
os.environ["LOG_FILE"] = "custom_ai_agent.log"
os.environ["LOG_DESTINATION"] = "file"

# Log messages at various levels
logger.debug("Debug message: Starting process...")
logger.info("Info message: Process is running.")
logger.warning("Warning message: Check this condition.")
logger.error("Error message: Something went wrong!")
logger.critical("Critical message: Immediate attention required!")

```

### Example: Logging to Syslog
```
# example_syslog_logging.py
import os
from utils.logger import logger

# Configure the logger to use syslog
os.environ["LOG_DESTINATION"] = "syslog"

# Log messages that will be sent to the system's syslog
logger.info("Syslog Info: This message is logged to syslog.")
logger.error("Syslog Error: An error has occurred.")
```
