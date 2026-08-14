from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_order_reviews_dataset.csv"
output_file = processed_data_path / "reviews_clean.csv"

data = pd.read_csv(input_file)

data["review_id"] = data["review_id"].astype("string")
data["order_id"] = data["order_id"].astype("string")

date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    data[column] = pd.to_datetime(
        data[column],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

data.to_csv(output_file, index=False)

print(f"Reviews transformed: {len(data)} rows")
print(f"Saved to: {output_file}")