from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_sellers_dataset.csv"
output_file = processed_data_path / "sellers_clean.csv"

data = pd.read_csv(input_file)

data["seller_id"] = data["seller_id"].astype("string")
data["seller_city"] = data["seller_city"].str.strip().str.lower()
data["seller_state"] = data["seller_state"].str.strip().str.upper()

data.to_csv(output_file, index=False)

print(f"Sellers transformed: {len(data)} rows")
print(f"Saved to: {output_file}")