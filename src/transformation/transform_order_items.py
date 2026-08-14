from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_order_items_dataset.csv"
output_file = processed_data_path / "order_items_clean.csv"

data = pd.read_csv(input_file)

data["order_id"] = data["order_id"].astype("string")
data["product_id"] = data["product_id"].astype("string")
data["seller_id"] = data["seller_id"].astype("string")

data["shipping_limit_date"] = pd.to_datetime(
    data["shipping_limit_date"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

data.to_csv(output_file, index=False)

print(f"Order Items transformed: {len(data)} rows")
print(f"Saved to: {output_file}")