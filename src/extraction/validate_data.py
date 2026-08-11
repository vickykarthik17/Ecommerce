'''def validate_columns(data, expected):
    return list(data.columns) == expected'''
from pathlib import Path

import pandas as pd

from expected_columns import expected_columns

project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"

for csv_file in sorted(raw_data_path.glob("*.csv")):
    data = pd.read_csv(csv_file)

    columns_valid = list(data.columns) == expected_columns[csv_file.name]
    rows_valid = len(data) > 0

    if columns_valid and rows_valid:
        status = "Valid"
    else:
        status = "Invalid"

    print(f"{csv_file.name}: {len(data)} rows, {len(data.columns)} columns, {status}")