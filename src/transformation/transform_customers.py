from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_customers_dataset.csv"
output_file = processed_data_path / "customers_clean.csv"

data = pd.read_csv(input_file)

data["customer_id"] = data["customer_id"].astype("string")
data["customer_unique_id"] = data["customer_unique_id"].astype("string")
data["customer_city"] = data["customer_city"].str.strip().str.lower()
data["customer_state"] = data["customer_state"].str.strip().str.upper()

data.to_csv(output_file, index=False)

print(f"Customers transformed: {len(data)} rows")
print(f"Saved to: {output_file}")
