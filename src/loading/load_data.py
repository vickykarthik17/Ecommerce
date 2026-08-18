from pathlib import Path
import pandas as pd
import psycopg

from db_config import DB_CONFIG

project_root=Path(__file__).resolve().parents[2]
processed_data_path=project_root/"data"/"processed"

def load_csv_to_postgres(file_name,table_name):
    file_path=processed_data_path/file_name
    data=pd.read_csv(file_path)
    data = data.astype(object).where(pd.notna(data), None)
    with psycopg.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            columns=", ".join(data.columns)
            placeholders=", ".join(["%s"] * len(data.columns))
            query=f""" INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
            """
            for row in data.itertuples(index=False,name=None):
                cursor.execute(query,row)
        connection.commit()
    print(f"Loaded {len(data)} rows into {table_name}")

if __name__=="__main__":
    load_csv_to_postgres(
        "category_translation_clean.csv",
        "category_translation"
    )