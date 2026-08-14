from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_order_payments_dataset.csv"
output_file = processed_data_path / "payments_clean.csv"

data = pd.read_csv(input_file)

data["order_id"] = data["order_id"].astype("string")

data["payment_type"] = (
    data["payment_type"]
    .str.strip()
    .str.lower()
)

data.to_csv(output_file, index=False)

print(f"Payments transformed: {len(data)} rows")
print(f"Saved to: {output_file}")