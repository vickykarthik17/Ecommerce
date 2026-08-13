from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_orders_dataset.csv"
output_file = processed_data_path / "orders_clean.csv"

data = pd.read_csv(input_file)

data["order_id"] = data["order_id"].astype("string")
data["customer_id"] = data["customer_id"].astype("string")
data["order_status"] = data["order_status"].str.strip().str.lower()

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    data[column] = pd.to_datetime(
        data[column],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

data.to_csv(output_file, index=False)

print(f"Orders transformed: {len(data)} rows")
print(f"Saved to: {output_file}")