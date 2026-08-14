from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "processed" / "reviews_clean.csv"

data = pd.read_csv(file_path)

print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

print(
    "Duplicate review_id + order_id:",
    data.duplicated(["review_id", "order_id"]).sum()
)

print("\nNull values:")
print(data.isnull().sum())

for column in ["review_creation_date", "review_answer_timestamp"]:
    data[column] = pd.to_datetime(data[column], errors="coerce")

print("\nData types:")
print(data.dtypes)