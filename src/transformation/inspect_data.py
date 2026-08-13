from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"

datasets = {
    "Customers": "olist_customers_dataset.csv",
    "Orders": "olist_orders_dataset.csv"
}

for name, file_name in datasets.items():
    file_path = raw_data_path / file_name
    data = pd.read_csv(file_path)

    print(f"\n{name}")
    print("Columns:", list(data.columns))
    print("\nData types:")
    print(data.dtypes)
    print("\nNull values:")
    print(data.isnull().sum())

    if name == "Customers":
        print("\nDuplicate customer_id:", data["customer_id"].duplicated().sum())
    else:
        print("\nDuplicate order_id:", data["order_id"].duplicated().sum())

    print("\nSample:")
    print(data.head(3))