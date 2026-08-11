from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
data_path = project_root / "data" / "raw" / "olist_geolocation_dataset.csv"

geolocation = pd.read_csv(data_path)

total_rows = len(geolocation)
duplicate_rows = geolocation.duplicated().sum()
unique_rows = geolocation.drop_duplicates().shape[0]

print(f"Total rows: {total_rows}")
print(f"Exact duplicate rows: {duplicate_rows}")
print(f"Rows after removing exact duplicates: {unique_rows}")