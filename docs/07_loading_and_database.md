07: Loading and PostgreSQL Database

1. Purpose

PostgreSQL is the target database for the transformed Olist datasets.

The loading stage takes the validated processed CSV files produced by the transformation layer and loads them into a relational PostgreSQL database.

The database schema uses primary keys, composite keys, foreign keys, and referential-integrity rules identified during data profiling and transformation.

2. Database

Database: ecommerce
PostgreSQL Version: 18

The database contains nine tables:

customers
orders
order_items
payments
reviews
products
sellers
geolocation
category_translation

The tables represent different business entities and transactional components of the Olist e-commerce dataset.

3. Loading Flow

The loading stage follows this sequence:

Processed CSV Files
        ↓
Reset Existing Target Tables
        ↓
Bulk Load Using PostgreSQL COPY
        ↓
Load Geolocation
        ↓
Database Validation

The complete process is orchestrated by:

src/run_pipeline.py

The main loading scripts are:

src/loading/load_data.py
src/loading/load_geolocation.py
src/loading/validate_database.py

4. Table Design

Customers

Table: customers

Primary Key:

customer_id

Stores customer-level information such as:

Customer identifier

Customer unique identifier

ZIP code prefix

City

State

Orders

Table: orders

Primary Key:

order_id

Foreign Key:

customer_id → customers.customer_id

Stores order-level information including:

Order status

Purchase timestamp

Approval timestamp

Carrier delivery date

Customer delivery date

Estimated delivery date

Order Items

Table: order_items

Composite Primary Key:

order_id + order_item_id

Foreign Keys:

order_id  → orders.order_id
product_id → products.product_id
seller_id  → sellers.seller_id

Stores individual products and sellers associated with each order.

The composite key is required because order_item_id identifies the item position within an order rather than uniquely identifying a row across the entire dataset.

Products

Table: products

Primary Key:

product_id

Stores product information such as:

Product category

Product name length

Product description length

Number of photos

Weight

Dimensions

Sellers

Table: sellers

Primary Key:

seller_id

Stores seller identifiers and location information.

Payments

Table: payments

Composite Primary Key:

order_id + payment_sequential

Foreign Key:

order_id → orders.order_id

Stores:

Payment method

Number of installments

Payment value

Multiple payment records can legitimately belong to the same order, so payment_sequential is part of the key.

Reviews

Table: reviews

Composite Primary Key:

review_id + order_id

Foreign Key:

order_id → orders.order_id

Stores:

Review score

Review comments

Review timestamps

The composite key is used because review_id alone was not unique in the source data.

Geolocation

Table: geolocation

Primary Key:

geolocation_id

The primary key is a PostgreSQL-generated identity column.

The ZIP code prefix is not used as the primary key because multiple geolocation records can share the same ZIP prefix while representing different geographic coordinates.

The processed geolocation dataset contains:

738,327 rows

from:

1,000,163 raw rows

Exact duplicate observations were removed during transformation, while legitimate repeated ZIP prefixes were preserved.

Category Translation

Table: category_translation

Primary Key:

product_category_name

Stores the English translation of product category names.

5. Relationship Structure

The main relational structure is:

customers
    |
    └── orders
          |
          ├── order_items ── products
          |        |
          |        └── sellers
          |
          ├── payments
          |
          └── reviews

products
    |
    └── category_translation

Geolocation is stored separately because ZIP code prefixes are not unique.

6. Key Design Decisions

Customer Key

customer_id

is the primary key for the customers table.

customer_unique_id is retained as a business identifier but is not used as the primary key.

Order Key

order_id

uniquely identifies an order.

Order Item Key

order_id + order_item_id

uniquely identifies an item within an order.

This preserves legitimate one-to-many order relationships instead of incorrectly treating repeated order_id values as duplicates.

Payment Key

order_id + payment_sequential

allows multiple payment records for the same order.

Review Key

review_id + order_id

is used because individual review IDs were repeated in the source data.

Geolocation Key

geolocation_id

is generated because ZIP prefixes can have multiple valid geographic records.

7. Referential Integrity

Foreign keys enforce the relationships between the main transactional tables.

The implemented relationships are:

orders.customer_id
    → customers.customer_id

order_items.order_id
    → orders.order_id

order_items.product_id
    → products.product_id

order_items.seller_id
    → sellers.seller_id

payments.order_id
    → orders.order_id

reviews.order_id
    → orders.order_id

These relationships were validated after loading.

8. Loading Strategy

The pipeline uses a full-refresh batch loading strategy.

The process is:

TRUNCATE existing target tables
        ↓
Load processed CSV files
        ↓
Validate database

This strategy is appropriate for the project because the Olist dataset is a static historical snapshot rather than a continuously changing production source.

It also makes repeated execution deterministic:

Same source data
      +
Same transformation rules
      ↓
Same target state

The full-refresh strategy avoids duplicate primary-key conflicts when the complete historical dataset is loaded again.

9. Bulk Loading

The processed CSV files are loaded using PostgreSQL COPY.

Bulk loading is used instead of inserting individual records one at a time because the project contains large datasets, particularly:

Geolocation: 738,327 rows
Order Items: 112,650 rows
Payments: 103,886 rows
Reviews: 99,224 rows
Orders: 99,441 rows
Customers: 99,441 rows

The bulk-loading approach provides a more appropriate ingestion method for these datasets.

10. Loading Order

The loading order respects the foreign-key dependencies.

The main tables are loaded as:

customers
    ↓
orders
    ↓
products
    ↓
sellers
    ↓
order_items
    ↓
payments
    ↓
reviews
    ↓
category_translation

Geolocation is loaded separately by:

src/loading/load_geolocation.py

The database is validated only after the required data has been loaded.

11. Database Validation

After loading, validate_database.py performs database-level checks.

Row Count Validation

The expected row counts are checked for all nine tables.

Latest successful run:

Table

Rows

customers

99,441

orders

99,441

order_items

112,650

payments

103,886

reviews

99,224

products

32,951

sellers

3,095

geolocation

738,327

category_translation

71

Key Validation

Primary and composite keys are checked for duplicates.

Latest result:

customers: PASS
orders: PASS
products: PASS
sellers: PASS
category_translation: PASS
order_items: PASS
payments: PASS
reviews: PASS

Foreign-Key Validation

The following relationships were checked:

orders → customers
order_items → orders
order_items → products
order_items → sellers
payments → orders
reviews → orders

Latest result:

orders → customers: PASS
order_items → orders: PASS
order_items → products: PASS
order_items → sellers: PASS
payments → orders: PASS
reviews → orders: PASS

12. Why Database Validation Is Separate

Transformation validation checks the processed CSV files before they enter the database.

Database validation checks the final loaded state.

Therefore, the pipeline has two distinct quality gates:

Processed CSV
      ↓
Transformation Validation
      ↓
PostgreSQL
      ↓
Database Validation

This catches problems that may only become visible after loading, such as:

Primary-key conflicts

Composite-key conflicts

Foreign-key violations

Unexpected database row counts

Referential-integrity failures

13. Result

The PostgreSQL database provides a structured relational target for the transformed Olist data.

The final database enforces:

Primary-key uniqueness

Composite-key uniqueness

Foreign-key relationships

Referential integrity

PostgreSQL-compatible data types

The latest end-to-end pipeline run completed successfully with all database key and foreign-key validations passing.

The pipeline completed in approximately:

69.48 seconds

14. Key Takeaway

The loading stage is not simply a CSV-to-database copy operation.

The database schema reflects decisions made earlier in the ETL process:

Data Profiling
      ↓
Business Meaning
      ↓
Key Identification
      ↓
Transformation
      ↓
Validation
      ↓
PostgreSQL Schema
      ↓
Bulk Loading
      ↓
Database Validation

This ensures that the target database structure is based on the actual relationships and characteristics discovered in the source data rather than arbitrary assumptions.