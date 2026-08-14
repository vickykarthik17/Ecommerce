from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"

file_path = processed_data_path / "order_items_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

print(
    "Duplicate order_id + order_item_id:",
    data.duplicated(
        ["order_id", "order_item_id"]
    ).sum()
)

print(f"Null order_id: {data['order_id'].isnull().sum()}")
print(f"Null product_id: {data['product_id'].isnull().sum()}")
print(f"Null seller_id: {data['seller_id'].isnull().sum()}")

print("\nNull values:")
print(data.isnull().sum())

data["shipping_limit_date"] = pd.to_datetime(
    data["shipping_limit_date"],
    errors="coerce"
)

print("\nData types:")
print(data.dtypes)

print("\nSample:")
print(data.head(3))