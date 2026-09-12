from contextlib import contextmanager

import psycopg

from loading.db_config import DB_CONFIG


PIPELINE_LOCK_KEY = 781245903


@contextmanager
def pipeline_database_lock():
    connection = psycopg.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pg_try_advisory_lock(%s)",
                (PIPELINE_LOCK_KEY,),
            )
            acquired = cursor.fetchone()[0]

        if not acquired:
            connection.close()
            yield False
            return

        yield True
    finally:
        if not connection.closed:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_advisory_unlock(%s)",
                    (PIPELINE_LOCK_KEY,),
                )
            connection.close()