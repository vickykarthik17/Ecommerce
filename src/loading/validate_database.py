import psycopg
from db_config import DB_CONFIG

with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:

        print("\n--- ROW COUNTS ---")

        for table in [
            "customers", "orders", "order_items", "payments",
            "reviews", "products", "sellers",
            "geolocation", "category_translation"
        ]:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"{table}: {cur.fetchone()[0]}")

        print("\n--- KEY VALIDATION ---")

        checks = [
            ("customers", "customer_id"),
            ("orders", "order_id"),
            ("products", "product_id"),
            ("sellers", "seller_id"),
            ("category_translation", "product_category_name"),
            ("order_items", "order_id, order_item_id"),
            ("payments", "order_id, payment_sequential"),
            ("reviews", "review_id, order_id")
        ]

        for table, key in checks:
            cur.execute(f"""
                SELECT COUNT(*) FROM (
                    SELECT {key}
                    FROM {table}
                    GROUP BY {key}
                    HAVING COUNT(*) > 1
                ) d
            """)
            print(f"{table}: {'PASS' if cur.fetchone()[0] == 0 else 'FAIL'}")

        print("\n--- FOREIGN KEY VALIDATION ---")

        relationships = [
            ("orders", "customer_id", "customers", "customer_id"),
            ("order_items", "order_id", "orders", "order_id"),
            ("order_items", "product_id", "products", "product_id"),
            ("order_items", "seller_id", "sellers", "seller_id"),
            ("payments", "order_id", "orders", "order_id"),
            ("reviews", "order_id", "orders", "order_id")
        ]

        for child, child_col, parent, parent_col in relationships:
            cur.execute(f"""
                SELECT COUNT(*)
                FROM {child} c
                LEFT JOIN {parent} p
                ON c.{child_col} = p.{parent_col}
                WHERE p.{parent_col} IS NULL
            """)
            print(
                f"{child} -> {parent}: "
                f"{'PASS' if cur.fetchone()[0] == 0 else 'FAIL'}"
            )

print("\nDatabase validation completed.")