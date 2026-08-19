from pathlib import Path
import psycopg
from db_config import DB_CONFIG


project_root = Path(__file__).resolve().parents[2]
processed_data_path = project_root / "data" / "processed"


def load_csv_to_postgres(file_name, table_name, columns):
    file_path = processed_data_path / file_name

    with psycopg.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            column_list = ", ".join(columns)

            with open(file_path, "r", encoding="utf-8") as file:
                next(file)

                with cursor.copy(
                    f"""
                    COPY {table_name} ({column_list})
                    FROM STDIN
                    WITH (FORMAT CSV, NULL '')
                    """
                ) as copy:
                    for line in file:
                        copy.write(line)

        connection.commit()

    print(f"Loaded {file_name} into {table_name}")


if __name__ == "__main__":

    load_csv_to_postgres(
        "customers_clean.csv",
        "customers",
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ]
    )

    load_csv_to_postgres(
        "orders_clean.csv",
        "orders",
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    load_csv_to_postgres(
        "products_clean.csv",
        "products",
        [
            "product_id",
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    )

    load_csv_to_postgres(
        "sellers_clean.csv",
        "sellers",
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ]
    )

    load_csv_to_postgres(
        "order_items_clean.csv",
        "order_items",
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value"
        ]
    )

    load_csv_to_postgres(
        "payments_clean.csv",
        "payments",
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    )

    load_csv_to_postgres(
        "reviews_clean.csv",
        "reviews",
        [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp"
        ]
    )

    load_csv_to_postgres(
        "category_translation_clean.csv",
        "category_translation",
        [
            "product_category_name",
            "product_category_name_english"
        ]
    )