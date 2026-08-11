from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def profile_dataset(file_path):
    df = pd.read_csv(file_path)

    print(f"\nDataset: {file_path.name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nColumns:")
    print(list(df.columns))
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print(f"\nDuplicate Rows: {df.duplicated().sum()}")


def main():
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    for file_path in csv_files:
        profile_dataset(file_path)


if __name__ == "__main__":
    main()