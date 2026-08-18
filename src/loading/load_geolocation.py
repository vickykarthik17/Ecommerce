from pathlib import Path

import psycopg

from db_config import DB_CONFIG


project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "processed" / "geolocation_clean.csv"


with psycopg.connect(**DB_CONFIG) as connection:
    with connection.cursor() as cursor:
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)

            with cursor.copy("""
                COPY geolocation (
                    geolocation_zip_code_prefix,
                    geolocation_lat,
                    geolocation_lng,
                    geolocation_city,
                    geolocation_state
                )
                FROM STDIN WITH (FORMAT CSV)
            """) as copy:

                for line in file:
                    copy.write(line)

    connection.commit()

print("Loaded geolocation data successfully")