from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"

file_path = processed_data_path / "orders_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

print(f"Duplicate order_id: {data['order_id'].duplicated().sum()}")
print(f"Null order_id: {data['order_id'].isnull().sum()}")
print(f"Null customer_id: {data['customer_id'].isnull().sum()}")

print("\nNull values:")
print(data.isnull().sum())
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    data[column] = pd.to_datetime(data[column], errors="coerce")
print("\nData types:")
print(data.dtypes)

print("\nSample:")
print(data.head(3))