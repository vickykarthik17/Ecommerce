from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"
processed_data_path = project_root / "data" / "processed"

input_file = raw_data_path / "olist_products_dataset.csv"
output_file = processed_data_path / "products_clean.csv"

data = pd.read_csv(input_file)

data["product_id"] = data["product_id"].astype("string")

data["product_category_name"] = (
    data["product_category_name"]
    .str.strip()
    .str.lower()
)

data = data.rename(
    columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length"
    }
)

integer_columns = [
    "product_name_length",
    "product_description_length",
    "product_photos_qty"
]

for column in integer_columns:
    data[column] = data[column].apply(
        lambda x: "" if pd.isna(x) else str(int(x))
    )
    
data.to_csv(output_file, index=False)

print(f"Products Transformed : {len(data)} rows")
print(f"Saved to : {output_file}")