import logging
from pathlib import Path

# Find the project folder
project_root = Path(__file__).resolve().parents[1]

# Create the logs folder if it does not exist
log_folder = project_root / "logs"
log_folder.mkdir(exist_ok=True)

# Log file location
log_file = log_folder / "pipeline.log"


def setup_logger():
    """Create and configure the ETL pipeline logger."""

    logger = logging.getLogger("etl_pipeline")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Format for each log message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Write logs to the log file
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    # Also display logs in the terminal
    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Send logs to both file and terminal
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger