from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"

file_path = processed_data_path / "payments_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

print(
    "Duplicate order_id + payment_sequential:",
    data.duplicated(
        ["order_id", "payment_sequential"]
    ).sum()
)

print(f"Null order_id: {data['order_id'].isnull().sum()}")
print(f"Null payment_type: {data['payment_type'].isnull().sum()}")

print("\nNull values:")
print(data.isnull().sum())

print("\nData types:")
print(data.dtypes)

print("\nSample:")
print(data.head(3))

