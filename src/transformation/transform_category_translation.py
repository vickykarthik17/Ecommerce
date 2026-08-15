from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "product_category_name_translation.csv"
output_file = processed_data_path / "category_translation_clean.csv"

data = pd.read_csv(input_file)

data["product_category_name"] = (
    data["product_category_name"]
    .str.strip()
    .str.lower()
)

data["product_category_name_english"] = (
    data["product_category_name_english"]
    .str.strip()
    .str.lower()
)

data.to_csv(output_file, index=False)

print(f"Category Translation transformed: {len(data)} rows")
print(f"Saved to: {output_file}")