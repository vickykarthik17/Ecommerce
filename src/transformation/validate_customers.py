from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"

file_path = processed_data_path / "customers_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")
print(f"Duplicate customer_id: {data['customer_id'].duplicated().sum()}")
print(f"Null customer_id: {data['customer_id'].isnull().sum()}")
print(f"Null customer_unique_id: {data['customer_unique_id'].isnull().sum()}")
print(f"Null customer_city: {data['customer_city'].isnull().sum()}")
print(f"Null customer_state: {data['customer_state'].isnull().sum()}")