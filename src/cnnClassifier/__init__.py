import logging
import os
import sys

# Format String
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")

# Folder banane ke liye sahi function
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,  # INFO capital me hoga
    format=logging_str,  # Missing comma lagaya
    handlers=[
        logging.FileHandler(log_filepath),  # File me save karega
        logging.StreamHandler(sys.stdout),  # Terminal par dikhayega
    ],
)

# Custom Logger Instance
logger = logging.getLogger("cnnclassification")

# Testing ke liye example
logger.info("Logging setup successfully complete ho gaya hai!")