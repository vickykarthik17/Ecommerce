import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

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

for step in steps:
    print(f"Running: {step}")

    result = subprocess.run(
        [sys.executable, str(project_root / step)],
        cwd=project_root
    )

    if result.returncode != 0:
        print(f"Pipeline failed: {step}")
        sys.exit(result.returncode)

print("Pipeline completed successfully.")