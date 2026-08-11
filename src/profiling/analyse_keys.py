from pathlib import Path
import pandas as pd

PROJECT_ROOT=Path(__file__).resolve().parents[2]
RAW_DATA_DIR=PROJECT_ROOT/"data"/"raw"


def check_key(df,key_columns):
    null_count=df[key_columns].isnull().sum()
    duplicate_count=df.duplicated(subset=key_columns).sum()
    print(f"Key: {', '.join(key_columns)}")
    print(f"Null Records: {null_count}")
    print(f"Duplicate records: {duplicate_count}")
    print()

def load_data(file_name):
    return pd.read_csv(RAW_DATA_DIR/file_name)

def main():
    customers = load_data("olist_customers_dataset.csv")
    orders = load_data("olist_orders_dataset.csv")
    order_items = load_data("olist_order_items_dataset.csv")
    payments = load_data("olist_order_payments_dataset.csv")
    reviews = load_data("olist_order_reviews_dataset.csv")
    products = load_data("olist_products_dataset.csv")
    sellers = load_data("olist_sellers_dataset.csv")
    geolocation = load_data("olist_geolocation_dataset.csv")
    categories = load_data("product_category_name_translation.csv")

    print("Customers")
    check_key(customers, ["customer_id"])
    check_key(customers, ["customer_unique_id"])

    print("Orders")
    check_key(orders, ["order_id"])

    print("Order Items")
    check_key(order_items, ["order_id", "order_item_id"])

    print("Payments")
    check_key(payments, ["order_id", "payment_sequential"])

    print("Reviews")
    check_key(reviews, ["review_id"])
    check_key(reviews, ["order_id"])

    print("Products")
    check_key(products, ["product_id"])

    print("Sellers")
    check_key(sellers, ["seller_id"])

    print("Geolocation")
    check_key(geolocation, ["geolocation_zip_code_prefix"])

    print("Category Translation")
    check_key(categories, ["product_category_name"])


if __name__ == "__main__":
    main()