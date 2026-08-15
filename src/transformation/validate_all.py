from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"

datasets = {
    "customers_clean.csv": ["customer_id"],
    "orders_clean.csv": ["order_id"],
    "order_items_clean.csv": ["order_id", "order_item_id"],
    "payments_clean.csv": ["order_id", "payment_sequential"],
    "reviews_clean.csv": ["review_id", "order_id"],
    "products_clean.csv": ["product_id"],
    "sellers_clean.csv": ["seller_id"],
    "geolocation_clean.csv": None,
    "category_translation_clean.csv": ["product_category_name"]
}

for file_name, key_columns in datasets.items():
    file_path = processed_data_path / file_name

    if not file_path.exists():
        print(f"{file_name}: Missing")
        continue

    data = pd.read_csv(file_path)

    print(f"\n{file_name}")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")
    print(f"Null values: {data.isnull().sum().sum()}")

    if key_columns:
        duplicate_count = data.duplicated(key_columns).sum()
        print(f"Duplicate key: {duplicate_count}")

print("\nOverall validation completed")