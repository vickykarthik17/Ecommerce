07: Transformation Rules

1. Purpose

This document defines the transformation rules applied to the nine Olist datasets before loading them into PostgreSQL.

The transformations focus on:

Standardizing data types

Cleaning text fields

Handling missing values appropriately

Removing exact duplicate records where required

Renaming inconsistent source columns

Preserving valid business data

Preparing CSV files for PostgreSQL loading

2. Transformation Flow

Raw CSV Files
     :
     ↓
Read Dataset
     :
     ↓
Standardize Data Types
     :
     ↓
Clean Text Fields
     :
     ↓
Handle Missing Values
     :
     ↓
Remove Exact Duplicates Where Required
     :
     ↓
Save Clean CSV
     :
     ↓
Data Quality Validation
     :
     ↓
PostgreSQL Loading

3. Customers

Source: olist_customers_dataset.csv
Output: customers_clean.csv

Transformations

customer_id converted to string.

customer_unique_id converted to string.

customer_zip_code_prefix preserved as the source ZIP prefix.

customer_city converted to lowercase.

customer_state converted to uppercase.

Validation

customer_id must be unique.

Required identifiers must not be null.

Row count is preserved.

4. Orders

Source: olist_orders_dataset.csv
Output: orders_clean.csv

Transformations

order_id converted to string.

customer_id converted to string.

order_status converted to lowercase.

Order timestamp columns converted to datetime values.

Missing order dates are preserved as null values.

Validation

order_id must be unique.

Date columns must contain valid datetime values or nulls.

Expected missing dates are not treated as errors.

5. Order Items

Source: olist_order_items_dataset.csv
Output: order_items_clean.csv

Transformations

order_id converted to string.

product_id converted to string.

seller_id converted to string.

shipping_limit_date converted to datetime.

Numeric price and freight columns preserved as numeric values.

Key

The combination of:

order_id + order_item_id

is treated as the unique order-item key.

6. Payments

Source: olist_order_payments_dataset.csv
Output: payments_clean.csv

Transformations

order_id converted to string.

payment_type converted to lowercase.

Numeric payment fields preserved as numeric values.

Key

The combination of:

order_id + payment_sequential

is treated as the unique payment key.

7. Reviews

Source: olist_order_reviews_dataset.csv
Output: reviews_clean.csv

Transformations

review_id converted to string.

order_id converted to string.

Review date columns converted to datetime.

Review comments are preserved as optional text fields.

Missing review comments are retained as null values.

Key

The combination of:

review_id + order_id

is used as the unique review key.

Important Data Quality Finding

Individual review_id values can appear more than once in the source data.

Therefore, review_id alone is not treated as the unique row identifier.

8. Products

Source: olist_products_dataset.csv
Output: products_clean.csv

Transformations

product_id converted to string.

product_category_name converted to lowercase.

Source column product_name_lenght renamed to product_name_length.

Source column product_description_lenght renamed to product_description_length.

Integer attributes are written as integer values instead of decimal strings.

Missing product attributes are preserved as null values.

PostgreSQL Compatibility

During loading, values such as:

40.0
287.0

caused PostgreSQL integer columns to reject the CSV values.

The transformation was therefore updated so integer attributes are written as:

40
287

while missing values remain blank and are loaded as SQL NULL.

9. Sellers

Source: olist_sellers_dataset.csv
Output: sellers_clean.csv

Transformations

seller_id converted to string.

seller_city converted to lowercase.

seller_state converted to uppercase.

ZIP prefix preserved.

Validation

seller_id must be unique.

Required identifiers must not be null.

10. Geolocation

Source: olist_geolocation_dataset.csv
Output: geolocation_clean.csv

Transformations

geolocation_city converted to lowercase.

geolocation_state converted to uppercase.

Exact duplicate rows removed.

Important Data Quality Decision

The source contains multiple records for the same ZIP code prefix.

These records were not removed simply because the ZIP prefix was repeated.

Investigation showed that the same ZIP prefix can contain different geographic coordinates.

Therefore:

Repeated ZIP prefix ≠ duplicate record

Only exact duplicate rows were removed.

Result

Source rows:

1,000,163

After exact duplicate removal:

738,327

11. Category Translation

Source: product_category_name_translation.csv
Output: category_translation_clean.csv

Transformations

Category names converted to lowercase.

Leading and trailing whitespace removed.

Translation values preserved.

Key

product_category_name is treated as the unique key.

12. Missing Value Handling

Missing values were handled according to their meaning rather than automatically removing rows.

Expected Missing Values

Orders

Some delivery-related dates are missing because certain orders did not reach those stages.

Reviews

Review titles and messages are optional and can legitimately be missing.

Products

Some product attributes are missing in the source dataset.

Rule

Missing value ≠ invalid record

A value is only treated as a data-quality problem when the missing value violates a required business or database constraint.

13. Duplicate Handling

Duplicate handling was performed based on the meaning of each dataset.

Exact Duplicates

Exact duplicate geolocation records were removed.

Business Keys

The following keys were validated after transformation:

Dataset

Key

Customers

customer_id

Orders

order_id

Products

product_id

Sellers

seller_id

Category Translation

product_category_name

Order Items

order_id + order_item_id

Payments

order_id + payment_sequential

Reviews

review_id + order_id

14. Transformation Validation

After all transformations, validate_all.py checks:

Row counts

Required null values

Duplicate business keys

Dataset-level validation rules

The final transformed datasets passed the configured validation checks.

15. Output

All transformed datasets are stored in:

data/
└── processed/

The processed files are then used by the PostgreSQL loading stage.

16. Key Transformation Principles

The transformation stage follows four main principles:

Preserve valid business data

Standardize data consistently

Remove only confirmed duplicates

Prepare data for reliable PostgreSQL loading

The goal is not to aggressively clean the dataset, but to make the data consistent, valid, and suitable for the downstream ETL stages.