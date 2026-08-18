import psycopg

from db_config import DB_CONFIG

try:
    with psycopg.connect(**DB_CONFIG) as connection:
        print("PostgreSQL connection successful")
        print(f"Database: {DB_CONFIG['dbname']}")

except Exception as error:
    print("PostgreSQL connection failed")
    print(error)