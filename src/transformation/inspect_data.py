from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"

datasets = {
    "Category Translation": "product_category_name_translation.csv"
}


for name, file_name in datasets.items():
    file_path = raw_data_path / file_name
    data = pd.read_csv(file_path)

    print(f"\n{name}")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")
    print("Columns:", list(data.columns))

    print("\nData types:")
    print(data.dtypes)

    print("\nNull values:")
    print(data.isnull().sum())

    print(
    "\nDuplicate product_category_name:",
    data["product_category_name"].duplicated().sum())

    print("\nSample:")
    print(data.head(3))