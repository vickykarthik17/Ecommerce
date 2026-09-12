import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


def _required_setting(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required database setting is missing: {name}")
    return value


DB_CONFIG = {
    "host": _required_setting("DB_HOST"),
    "port": _required_setting("DB_PORT"),
    "dbname": _required_setting("DB_NAME"),
    "user": _required_setting("DB_USER"),
    "password": _required_setting("DB_PASSWORD"),
    "connect_timeout": 5,
}


DATASET_TABLES = [
    "orders",
    "customers",
    "order_items",
    "payments",
    "reviews",
    "products",
    "sellers",
    "geolocation",
    "category_translation",
]


def get_dataset_counts():
    counts = {}

    with psycopg.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:

            for table in DATASET_TABLES:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table}"
                )

                counts[table] = cursor.fetchone()[0]

    return counts