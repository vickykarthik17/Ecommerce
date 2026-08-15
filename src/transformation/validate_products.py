from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "processed" / "products_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

print(
    "Duplicate product_id:",
    data["product_id"].duplicated().sum()
)

print("\nNull values:")
print(data.isnull().sum())

print("\nColumns:")
print(list(data.columns))