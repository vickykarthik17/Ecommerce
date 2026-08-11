from pathlib import Path
import pandas as pd

PROJECT_ROOT=Path(__file__).resolve().parents[2]
RAW_DATA_DIR=PROJECT_ROOT/"data"/"raw"

def load_data(file_name):
    return pd.read_csv(RAW_DATA_DIR/file_name)

def check_relationship(parent_df,child_df,parent_key,child_key):
    parent_keys=set(parent_df[parent_key].dropna())
    child_keys=set(child_df[child_key].dropna())
    orphan_keys=child_keys-parent_keys
    print(f"{child_key} -> {parent_key}")
    print(f"Orphan_records: {len(orphan_keys)}")
    print()

def main():
    customers=load_data("olist_customers_dataset.csv")
    orders=load_data("olist_orders_dataset.csv")
    order_items=load_data("olist_order_items_dataset.csv")
    products=load_data("olist_products_dataset.csv")
    sellers=load_data("olist_sellers_dataset.csv")
    payments=load_data("olist_order_payments_dataset.csv")
    reviews=load_data("olist_order_reviews_dataset.csv")

    check_relationship(customers,orders,"customer_id","customer_id")
    check_relationship(orders,order_items,"order_id","order_id")
    check_relationship(products,order_items,"product_id","product_id")
    check_relationship(sellers,order_items,"seller_id","seller_id")
    check_relationship(orders,payments,"order_id","order_id")
    check_relationship(orders,reviews,"order_id","order_id")


if __name__ == "__main__":
    main()


