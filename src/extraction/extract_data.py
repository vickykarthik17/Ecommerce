from pathlib import Path

import pandas as pd

from expected_columns import expected_columns
from validate_data import validate_columns


project_root = Path(__file__).resolve().parents[2]
raw_data_path = project_root / "data" / "raw"

expected_files = list(expected_columns.keys())

print("Extraction started")
print()

for file_name in expected_files:
    file_path = raw_data_path / file_name

    if not file_path.exists():
        print(f"{file_name}: File not found")
        continue

    try:
        data = pd.read_csv(file_path)
    except Exception:
        print(f"{file_name}: Could not read file")
        continue

    if data.empty:
        print(f"{file_name}: Empty dataset")
        continue

    if not validate_columns(data, expected_columns[file_name]):
        print(f"{file_name}: Unexpected columns")
        continue

    print(f"{file_name}: {len(data)} rows, {len(data.columns)} columns, Valid")

print()
print("Extraction completed")