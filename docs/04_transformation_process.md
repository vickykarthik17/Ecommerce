04: Transformation Process

1. Purpose

This document explains the transformation rules applied to the nine Olist datasets before loading them into PostgreSQL.

The transformation stage is not based on blindly removing NULLs, duplicates, or repeated identifiers. The rules were defined after profiling the source data and understanding the business meaning of each dataset.

The main objectives are:

Standardize data types.

Clean and normalize selected text fields.

Convert date columns to appropriate datetime values.

Handle missing values according to their meaning.

Remove only confirmed exact duplicate observations.

Preserve valid one-to-many business relationships.

Rename inconsistent source columns.

Resolve PostgreSQL datatype compatibility issues.

Produce consistent processed CSV files for validation and loading.

2. Transformation Flow

Raw CSV Files
      ↓
Read Dataset
      ↓
Understand / Apply Dataset-Specific Rules
      ↓
Standardize Data Types
      ↓
Clean Text Fields
      ↓
Handle Missing Values
      ↓
Remove Confirmed Exact Duplicates
      ↓
Save Processed CSV
      ↓
Transformation Validation
      ↓
PostgreSQL Loading

Each dataset has its own transformation script because the meaning of identifiers, missing values, and duplicates differs between datasets.

3. Transformation Philosophy

The central rule followed during transformation was:

Understand the data
        ↓
Profile the data
        ↓
Determine business meaning
        ↓
Define transformation rule
        ↓
Validate the result

For example, a repeated identifier is not automatically considered a duplicate.

An order_id can legitimately appear multiple times in the order-items dataset because one order can contain multiple items.

Similarly, a ZIP code prefix can appear multiple times in the geolocation dataset because one prefix can correspond to multiple geographic coordinates.

Therefore:

Repeated value ≠ duplicate record

A record was removed only when the profiling and business meaning supported treating it as an exact duplicate.

4. Customers

Source: olist_customers_dataset.csv
Output: customers_clean.csv

Transformations

customer_id converted to string.

customer_unique_id converted to string.

customer_zip_code_prefix preserved as the source ZIP prefix.

customer_city converted to lowercase.

customer_state converted to uppercase.

Key

customer_id

is treated as the primary business key for the processed customer dataset.

Validation

customer_id must be unique.

Required identifiers must not be null.

Row count is preserved.

5. Orders

Source: olist_orders_dataset.csv
Output: orders_clean.csv

Transformations

order_id converted to string.

customer_id converted to string.

order_status converted to lowercase.

Order timestamp columns converted to datetime values.

Missing order dates are preserved as null values.

Key

order_id

is treated as the unique order key.

Validation

order_id must be unique.

Date columns must contain valid datetime values or nulls.

Expected missing dates are not treated as errors.

Business Meaning

Some delivery-related dates can be missing because an order may not have reached that stage of its lifecycle.

Therefore:

Missing delivery date
        ≠
Invalid order

6. Order Items

Source: olist_order_items_dataset.csv
Output: order_items_clean.csv

Transformations

order_id converted to string.

product_id converted to string.

seller_id converted to string.

shipping_limit_date converted to datetime.

Numeric price and freight_value fields preserved as numeric values.

Key

The combination of:

order_id + order_item_id

is treated as the unique order-item key.

Business Meaning

An order can contain multiple items.

Therefore, repeated order_id values in this dataset are expected and must not be removed as duplicates.

order_id repeated
        ↓
Potentially valid one-to-many relationship

7. Payments

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

Business Meaning

An order can have multiple payment records.

Therefore, order_id alone is not sufficient to identify a payment record.

8. Reviews

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

Important Data-Quality Finding

Individual review_id values can appear more than once in the source data.

Therefore:

review_id alone
        ≠
unique row identifier

The composite key preserves the actual uniqueness identified during profiling.

Missing Values

Review titles and messages are optional fields and can legitimately be missing.

A missing review comment does not invalidate the review record.

9. Products

Source: olist_products_dataset.csv
Output: products_clean.csv

Transformations

product_id converted to string.

product_category_name converted to lowercase.

product_name_lenght renamed to product_name_length.

product_description_lenght renamed to product_description_length.

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

while missing values remain blank and can be loaded as SQL NULL.

This is an example of a transformation rule being driven by an actual downstream database compatibility issue rather than arbitrary cleaning.

10. Sellers

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

11. Geolocation

Source: olist_geolocation_dataset.csv
Output: geolocation_clean.csv

This dataset required additional investigation because the raw source contained a very large number of records and repeated ZIP code prefixes.

Transformations

geolocation_city converted to lowercase.

geolocation_state converted to uppercase.

Exact duplicate rows removed.

Important Data-Quality Investigation

The source contains multiple records for the same ZIP code prefix.

These records were not removed simply because the ZIP prefix was repeated.

Investigation showed that the same ZIP prefix can contain different geographic coordinates.

Therefore:

Repeated ZIP prefix
        ≠
Duplicate record

Only exact duplicate rows were removed.

Result

Raw source:

1,000,163 rows

After exact duplicate removal:

738,327 rows

The transformation therefore removes confirmed redundant observations while preserving valid geographic records.

12. Category Translation

Source: product_category_name_translation.csv
Output: category_translation_clean.csv

Transformations

Category names converted to lowercase.

Leading and trailing whitespace removed.

Translation values preserved.

Key

product_category_name

is treated as the unique key.

13. Missing Value Handling

Missing values were handled according to their meaning rather than automatically removing rows.

Orders

Some delivery-related dates are missing because certain orders did not reach those stages of the order lifecycle.

Reviews

Review titles and messages are optional and can legitimately be missing.

Products

Some product attributes are missing in the source dataset.

General Rule

Missing value
      ≠
Invalid record

A value is treated as a data-quality problem only when its absence violates a required business or database constraint.

This prevents valid historical records from being removed unnecessarily.

14. Duplicate Handling

Duplicate handling was performed according to the meaning of each dataset.

Exact Duplicates

Exact duplicate geolocation records were removed.

Legitimate Repeated Identifiers

Repeated identifiers were preserved when they represented valid business relationships.

Examples:

orders
    ↓
order_items

One order can contain multiple order items.

Similarly:

orders
    ↓
payments

One order can have multiple payment records.

And:

ZIP prefix
    ↓
multiple geolocation records

A repeated ZIP prefix can represent different coordinates.

Business Keys Validated

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

15. Transformation Validation

After all transformations, validate_all.py checks the processed datasets.

The validation includes:

Row counts

Column counts

Null-value counts

Duplicate business keys

Dataset-level validation rules

The final transformed datasets completed the configured validation stage successfully.

The validation output is retained as a separate quality gate before PostgreSQL loading.

16. Processed Output

All transformed datasets are stored in:

data/
└── processed/

The processed files are then consumed by the PostgreSQL loading stage.

Examples include:

customers_clean.csv
orders_clean.csv
order_items_clean.csv
payments_clean.csv
reviews_clean.csv
products_clean.csv
sellers_clean.csv
geolocation_clean.csv
category_translation_clean.csv

17. Key Transformation Decisions

The most important transformation decisions were driven by observations made during profiling.

Observation

Decision

order_id repeats in order items

Preserve because one order can contain multiple items

order_id repeats in payments

Preserve and use payment_sequential as part of the key

review_id is repeated

Use review_id + order_id

ZIP prefixes repeat in geolocation

Preserve valid records

Exact geolocation rows repeat

Remove exact duplicates

Product integer values appear as 40.0

Convert to integer-compatible 40

Delivery dates are missing

Preserve NULL when consistent with order lifecycle

Review comments are missing

Preserve NULL because comments are optional

Product attributes are missing

Preserve NULL unless a database rule requires otherwise

Source column names contain lenght

Rename to correctly defined target names

This table captures the main principle of the transformation stage:

Observed data issue
        ↓
Investigate
        ↓
Understand business meaning
        ↓
Define rule
        ↓
Transform
        ↓
Validate

18. Why We Did Not Clean Randomly

A common ETL mistake is to apply generic rules such as:

Remove every duplicate
Fill every NULL
Delete every repeated identifier

That approach was deliberately avoided.

For this project, the transformation rules were based on:

Source profiling.

Identifier analysis.

Relationship analysis.

Business meaning.

PostgreSQL schema requirements.

Validation results.

Actual loading errors encountered during development.

For example, removing every repeated order_id from order_items would destroy legitimate order-item records.

Likewise, removing every repeated geolocation ZIP prefix would remove valid geographic observations.

The goal was therefore not aggressive cleaning.

The goal was:

Make the data consistent, valid, and suitable for downstream processing while preserving legitimate business information.

19. Transformation Principles

The transformation stage follows four main principles:

1. Preserve valid business data

Do not remove a record merely because a value is repeated or missing.

2. Standardize consistently

Use consistent data types, text casing, date formats, and column names.

3. Remove only confirmed duplicates

An observation is removed as a duplicate only when the data and business meaning support that decision.

4. Prepare data for reliable database loading

The processed output must be compatible with the PostgreSQL schema and downstream validation rules.

20. Final Transformation Outcome

The transformation stage produces nine cleaned and standardized datasets that are ready for database loading.

The final process is:

Raw Olist Data
      ↓
Dataset-Specific Transformation
      ↓
Business-Meaning-Based Cleaning
      ↓
Data-Type Standardization
      ↓
Duplicate / NULL Handling
      ↓
PostgreSQL Compatibility
      ↓
Processed CSV Files
      ↓
Transformation Validation
      ↓
PostgreSQL Loading

The transformation layer therefore acts as the bridge between the raw historical source data and the structured PostgreSQL database.