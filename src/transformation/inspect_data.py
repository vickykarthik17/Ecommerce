from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"

datasets = {
    "Reviews": "olist_order_reviews_dataset.csv"
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

if name == "Reviews":
    print(
        "\nDuplicate review_id + order_id:",
        data.duplicated(
            ["review_id", "order_id"]
        ).sum()
    )

    print("\nSample:")
    print(data.head(3))