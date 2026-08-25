import subprocess
import sys
import time
from pathlib import Path

from logging_config import setup_logger


project_root = Path(__file__).resolve().parents[1]

logger = setup_logger()


steps = [
    "src/extraction/extract_data.py",
    "src/extraction/validate_data.py",

    "src/transformation/transform_customers.py",
    "src/transformation/transform_orders.py",
    "src/transformation/transform_order_items.py",
    "src/transformation/transform_payments.py",
    "src/transformation/transform_reviews.py",
    "src/transformation/transform_products.py",
    "src/transformation/transform_sellers.py",
    "src/transformation/transform_geolocation.py",
    "src/transformation/transform_category_translation.py",

    "src/transformation/validate_all.py",

    "src/loading/load_data.py",
    "src/loading/load_geolocation.py",
    "src/loading/validate_database.py"
]


logger.info("Pipeline started")

pipeline_start = time.time()


for step in steps:

    logger.info(f"Running: {step}")

    step_start = time.time()

    result = subprocess.run(
        [sys.executable, str(project_root / step)],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    # Display normal output in the terminal
    if result.stdout:
        print(result.stdout, end="")

    step_time = time.time() - step_start

    if result.returncode != 0:

        # Record the actual error in the log
        if result.stderr:
            logger.error(
                f"Error output from {step}:\n"
                f"{result.stderr.strip()}"
            )

        logger.error(
            f"Pipeline failed at: {step} "
            f"after {step_time:.2f} seconds"
        )

        sys.exit(result.returncode)

    logger.info(
        f"Completed: {step} "
        f"in {step_time:.2f} seconds"
    )

pipeline_time = time.time() - pipeline_start

logger.info(
    f"Pipeline completed successfully in "
    f"{pipeline_time:.2f} seconds"
)
