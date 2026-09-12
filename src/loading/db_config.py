import os

from dotenv import load_dotenv

load_dotenv()


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