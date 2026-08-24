# E-Commerce ETL Pipeline
## Data Dictionary, Data Quality and ETL Decisions

## 1. Project Overview

**Project:** E-Commerce ETL Pipeline
**Dataset:** Olist Brazilian E-Commerce Public Dataset  
**Language:** Python  
**Database:** PostgreSQL 18  
**Pipeline Type:** Batch ETL  

### Objective

The project builds a reusable end-to-end ETL pipeline that:

1. Extracts the nine raw Olist CSV datasets.
2. Validates the source structure and data.
3. Transforms and standardizes the datasets.
4. Validates the transformed data.
5. Loads the processed data into PostgreSQL.
6. Validates keys and relationships in the database.
7. Records execution status, timings, and errors through logging.

The raw source files are not modified. Transformations are applied to processed copies.

---

# 2. Why This Dataset?

The Olist dataset was selected because it represents a realistic e-commerce marketplace and contains multiple related entities rather than a single flat table.

It includes:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Category translations

This provides realistic ETL scenarios involving:

- One-to-many relationships
- Primary and composite keys
- Missing values
- Duplicate records
- Different data types
- Date fields
- Text standardization
- Relational database constraints

The dataset is a static historical snapshot, so the pipeline is implemented as a reusable batch process rather than a continuously running ingestion system.

---

# 3. ETL Architecture

```text
Olist CSV Files
       |
       v
   Extraction
       |
       v
Source Validation
       |
       v
 Transformation
       |
       v
Data Quality Validation
       |
       v
PostgreSQL Full Refresh
       |
       v
 Database Validation
       |
       v
 Logging / Error Handling
```

The main orchestration file is:

```text
src/run_pipeline.py
```

The pipeline executes each stage in sequence and stops when a stage fails.

---

# 4. Source Dataset Overview

| Dataset | Source Rows | Columns | Processed Rows |
|---|---:|---:|---:|
| Customers | 99,441 | 5 | 99,441 |
| Orders | 99,441 | 8 | 99,441 |
| Order Items | 112,650 | 7 | 112,650 |
| Payments | 103,886 | 5 | 103,886 |
| Reviews | 99,224 | 7 | 99,224 |
| Products | 32,951 | 9 | 32,951 |
| Sellers | 3,095 | 4 | 3,095 |
| Geolocation | 1,000,163 | 5 | 738,327 |
| Category Translation | 71 | 2 | 71 |

The reduction in the geolocation dataset is caused by removing exact duplicate rows.

---

# 5. Source Data Dictionary

## 5.1 Customers

**File:** `olist_customers_dataset.csv`

**Purpose:** Stores customer information.

| Column | Description |
|---|---|
| `customer_id` | Identifier for the customer record |
| `customer_unique_id` | Identifier representing the customer across orders |
| `customer_zip_code_prefix` | Customer ZIP code prefix |
| `customer_city` | Customer city |
| `customer_state` | Customer state |

### Key Decision

`customer_id` is unique and is used as the primary key.

`customer_unique_id` can repeat and is therefore not treated as an order-level key.

### Relationship

```text
customers.customer_id
        |
        v
orders.customer_id
```
---

## 5.2 Orders

**File:** `olist_orders_dataset.csv`

**Purpose:** Stores order-level information.

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_id` | Customer who placed the order |
| `order_status` | Order status |
| `order_purchase_timestamp` | Time when the order was placed |
| `order_approved_at` | Order approval timestamp |
| `order_delivered_carrier_date` | Date handed to carrier |
| `order_delivered_customer_date` | Date delivered to customer |
| `order_estimated_delivery_date` | Estimated delivery date |

### Key Decision

`order_id` is the primary key.

Some date fields contain null values. These are preserved because missing dates can be meaningful depending on the order status.

### Relationships

```text
orders.order_id
      |
      +--> order_items.order_id
      +--> payments.order_id
      +--> reviews.order_id
```
---

## 5.3 Order Items

**File:** `olist_order_items_dataset.csv`

**Purpose:** Stores the products included in orders.

| Column | Description |
|---|---|
| `order_id` | Order identifier |
| `order_item_id` | Item sequence within an order |
| `product_id` | Product identifier |
| `seller_id` | Seller identifier |
| `shipping_limit_date` | Shipping deadline |
| `price` | Product price |
| `freight_value` | Freight/shipping cost |

### Key Decision

`order_id` is not unique because an order can contain multiple items.

The composite primary key is:

```text
(order_id, order_item_id)
```

### Relationships

```text
order_items.order_id
        |
        v
orders.order_id

order_items.product_id
        |
        v
products.product_id

order_items.seller_id
        |
        v
sellers.seller_id
```
---

## 5.4 Payments

**File:** `olist_order_payments_dataset.csv`

**Purpose:** Stores payment information.

| Column | Description |
|---|---|
| `order_id` | Order identifier |
| `payment_sequential` | Payment sequence number |
| `payment_type` | Payment method |
| `payment_installments` | Number of installments |
| `payment_value` | Payment amount |

### Key Decision

An order can have multiple payment records.

The composite primary key is:

```text
(order_id, payment_sequential)
```

### Relationship

```text
payments.order_id
       |
       v
orders.order_id
```
---

## 5.5 Reviews

**File:** `olist_order_reviews_dataset.csv`

**Purpose:** Stores customer review information.

| Column | Description |
|---|---|
| `review_id` | Review identifier |
| `order_id` | Related order |
| `review_score` | Customer rating |
| `review_comment_title` | Review title |
| `review_comment_message` | Review message |
| `review_creation_date` | Review creation date |
| `review_answer_timestamp` | Review response timestamp |

### Key Finding

Profiling showed:

- `review_id` has 814 repeated values.
- `order_id` has 551 repeated values.
- `(review_id, order_id)` has no duplicates.

Therefore, individual identifiers were not used to remove records.

The composite key is:

```text
(review_id, order_id)
```

Review comment fields contain many null values. They are optional fields and are preserved.

---

## 5.6 Products

**File:** `olist_products_dataset.csv`

**Purpose:** Stores product information.

| Column | Description |
|---|---|
| `product_id` | Product identifier |
| `product_category_name` | Product category |
| `product_name_length` | Product name length |
| `product_description_length` | Description length |
| `product_photos_qty` | Number of product photos |
| `product_weight_g` | Product weight |
| `product_length_cm` | Product length |
| `product_height_cm` | Product height |
| `product_width_cm` | Product width |

### Source Naming Issue

The source contains:

```text
product_name_lenght
product_description_lenght
```

These are renamed to:

```text
product_name_length
product_description_length
```

### Key Decision

`product_id` is the primary key.

Missing product attributes are preserved.

---

## 5.7 Sellers

**File:** `olist_sellers_dataset.csv`

**Purpose:** Stores seller information.

| Column | Description |
|---|---|
| `seller_id` | Seller identifier |
| `seller_zip_code_prefix` | Seller ZIP code prefix |
| `seller_city` | Seller city |
| `seller_state` | Seller state |

`seller_id` is unique and is used as the primary key.

---

## 5.8 Geolocation

**File:** `olist_geolocation_dataset.csv`

**Source rows:** 1,000,163  
**Processed rows:** 738,327

**Purpose:** Stores geographic observations associated with ZIP code prefixes.

| Column | Description |
|---|---|
| `geolocation_zip_code_prefix` | ZIP code prefix |
| `geolocation_lat` | Latitude |
| `geolocation_lng` | Longitude |
| `geolocation_city` | City |
| `geolocation_state` | State |

### Data Quality Findings

Profiling identified:

- 19,015 unique ZIP prefixes.
- 17,972 ZIP prefixes have multiple records.
- 261,836 exact duplicate rows.

A repeated ZIP prefix does not automatically indicate a duplicate business record. The same ZIP prefix can have different geographic coordinates.

### Transformation Decision

Only exact duplicate rows are removed.

```text
Exact duplicate
      |
      v
    Remove

Same ZIP prefix
+ different coordinates
      |
      v
     Keep
```

The PostgreSQL table therefore does not use the ZIP prefix as a primary key.

A generated `geolocation_id` is used as the surrogate primary key.

---

## 5.9 Category Translation

**File:** `product_category_name_translation.csv`

**Purpose:** Stores English translations for product categories.

| Column | Description |
|---|---|
| `product_category_name` | Original category name |
| `product_category_name_english` | English category name |

`product_category_name` is used as the primary key.

---

# 6. Data Quality Rules

The transformation process applies rules based on the meaning of each dataset.

| Issue | Decision |
|---|---|
| Repeated `customer_unique_id` | Preserve |
| Missing order dates | Preserve as null |
| Repeated `review_id` | Use composite key |
| Missing review comments | Preserve |
| Missing product attributes | Preserve |
| Product source column misspellings | Rename |
| Exact geolocation duplicates | Remove |
| Repeated geolocation ZIP prefixes | Preserve |

The principle is to distinguish between **invalid duplicates** and **valid repeated observations** rather than removing data based only on frequency.

---

# 7. Transformation Rules

## Customers

- Convert identifiers to strings.
- Convert cities to lowercase.
- Convert states to uppercase.

## Orders

- Convert identifiers to strings.
- Convert order status to lowercase.
- Parse date columns.
- Preserve meaningful null dates.

## Order Items

- Convert identifiers to strings.
- Parse `shipping_limit_date`.
- Preserve the composite key.

## Payments

- Convert `order_id` to string.
- Convert `payment_type` to lowercase.

## Reviews

- Convert identifiers to strings.
- Parse review date fields.
- Preserve optional comments.
- Validate the composite key.

## Products

- Convert `product_id` to string.
- Convert category names to lowercase.
- Rename misspelled source columns.
- Preserve missing attributes.
- Format integer attributes correctly for PostgreSQL loading.

## Sellers

- Convert `seller_id` to string.
- Convert cities to lowercase.
- Convert states to uppercase.

## Geolocation

- Convert cities to lowercase.
- Convert states to uppercase.
- Remove exact duplicate rows.
- Preserve repeated ZIP-prefix observations.

## Category Translation

- Standardize category names.
- Preserve category translations.

---

# 8. PostgreSQL Design

The database is:

```text
ecommerce
```

The PostgreSQL schema contains:

```text
customers
orders
order_items
payments
reviews
products
sellers
geolocation
category_translation
```

### Primary Keys

| Table | Primary Key |
|---|---|
| `customers` | `customer_id` |
| `orders` | `order_id` |
| `order_items` | `order_id, order_item_id` |
| `payments` | `order_id, payment_sequential` |
| `reviews` | `review_id, order_id` |
| `products` | `product_id` |
| `sellers` | `seller_id` |
| `geolocation` | `geolocation_id` |
| `category_translation` | `product_category_name` |

### Foreign Keys

```text
orders.customer_id
    -> customers.customer_id

order_items.order_id
    -> orders.order_id

order_items.product_id
    -> products.product_id

order_items.seller_id
    -> sellers.seller_id

payments.order_id
    -> orders.order_id

reviews.order_id
    -> orders.order_id
```

The geolocation ZIP prefix is not defined as a foreign key because it is not unique.

---

# 9. Loading Strategy

The project uses PostgreSQL `COPY` for bulk loading.

### Why COPY?

The source contains datasets with more than 100,000 rows. Row-by-row inserts would create unnecessary database operations.

`COPY` is therefore used to load processed CSV files efficiently.

### Full Refresh

Before loading a complete batch, the target tables are reset using:

```sql
TRUNCATE TABLE ... CASCADE;
```

The processed files are then bulk loaded.

This provides repeatable execution for the static Olist dataset.

### Why Full Refresh?

The source is a historical static dataset rather than a continuously changing production source.

Therefore, the project does not require:

- Change Data Capture
- Incremental loading
- Upserts
- Daily scheduling
- Airflow
- Streaming ingestion

A full-refresh batch design is sufficient for the current project scope.

---

# 10. Database Validation

After loading, the pipeline validates:

1. Row counts
2. Primary keys
3. Composite keys
4. Foreign-key relationships
5. Orphan records

### Final Row Counts

| Table | Rows |
|---|---:|
| `customers` | 99,441 |
| `orders` | 99,441 |
| `order_items` | 112,650 |
| `payments` | 103,886 |
| `reviews` | 99,224 |
| `products` | 32,951 |
| `sellers` | 3,095 |
| `geolocation` | 738,327 |
| `category_translation` | 71 |

### Key Validation

All configured key checks passed.

### Relationship Validation

The following relationships passed:

```text
orders -> customers
order_items -> orders
order_items -> products
order_items -> sellers
payments -> orders
reviews -> orders
```

No orphan records were found.

---

# 11. Pipeline Orchestration

The main orchestration script is:

```text
src/run_pipeline.py
```

The execution order is:

```text
1. Extract
2. Validate source data
3. Transform customers
4. Transform orders
5. Transform order items
6. Transform payments
7. Transform reviews
8. Transform products
9. Transform sellers
10. Transform geolocation
11. Transform category translation
12. Validate transformed data
13. Reset PostgreSQL tables
14. Bulk load processed data
15. Load geolocation
16. Validate database
```

The orchestrator executes each script as a separate Python process.

If a process returns a non-zero exit code, the pipeline:

1. Captures the error.
2. Logs the failed step.
3. Stops execution.
4. Does not continue to later stages.

---

# 12. Logging and Error Handling

Logging is configured in:

```text
src/logging_config.py
```

The log file is:

```text
logs/pipeline.log
```

The logger records:

- Pipeline start
- Step name
- Step completion
- Step execution time
- Error output
- Failed stage
- Total pipeline completion time

Logs are written to both the terminal and the log file.

The `logs/` directory is excluded from Git because runtime logs are generated locally.

### Failure Test

A controlled exception was intentionally introduced into a transformation script.

The pipeline correctly:

```text
Detected failure
      |
      v
Captured traceback
      |
      v
Identified failed step
      |
      v
Stopped execution
```

The temporary test exception was then removed and the full pipeline was executed successfully.

---

# 13. Repeatability and Full End-to-End Testing

The complete pipeline was executed from extraction through final database validation.

The final run produced:

```text
customers: 99441
orders: 99441
order_items: 112650
payments: 103886
reviews: 99224
products: 32951
sellers: 3095
geolocation: 738327
category_translation: 71
```

All key checks passed.

All configured foreign-key checks passed.

The pipeline was also executed again after a controlled failure test, confirming that the pipeline recovered correctly after the temporary failure was removed.

---

# 14. Important Implementation Challenges

## Review Identifiers

### Problem

`review_id` and `order_id` individually contained repeated values.

### Investigation

The combination:

```text
review_id + order_id
```

was unique.

### Solution

The composite key was used instead of deleting records based on individual identifier repetition.

---

## Geolocation Duplicates

### Problem

The geolocation dataset contained 261,836 exact duplicate rows and many repeated ZIP prefixes.

### Investigation

Repeated ZIP prefixes can represent different geographic coordinates.

### Solution

Only exact duplicate rows were removed.

---

## Product Integer Loading

### Problem

Some integer values appeared as:

```text
40.0
```

in the processed CSV because Pandas could represent columns containing nulls as floating-point values.

PostgreSQL integer columns rejected these values.

### Solution

Integer attributes were explicitly converted to integer strings before CSV output, while blank values remained available for SQL NULL handling.

---

## PostgreSQL Loading Performance

### Problem

Row-by-row insertion would be inefficient for datasets containing tens or hundreds of thousands of records.

### Solution

PostgreSQL `COPY` was used for bulk loading.

---

## Repeatable Database Loading

### Problem

Re-running the pipeline against existing data could create duplicate-key conflicts.

### Solution

The loading stage uses a full-refresh approach:

```text
TRUNCATE
   |
   v
COPY
```

This makes complete batch reruns deterministic.

---

# 15. Current Project Status

The core ETL implementation is complete.

### Completed

- Source profiling
- Source data validation
- Extraction
- Transformation of all nine datasets
- Transformation validation
- PostgreSQL schema
- PostgreSQL bulk loading
- Full-refresh loading
- Database validation
- Key validation
- Foreign-key validation
- Orphan-record validation
- Pipeline orchestration
- Logging
- Error handling
- Controlled failure testing
- Repeatability testing
- End-to-end testing

### Current Scope

The project currently focuses on:

```text
Extraction
Transformation
Data Quality
PostgreSQL Loading
Validation
Orchestration
Logging
Error Handling
```



---

# 16. Key Interview Explanation

A concise explanation of the project is:

> I built an end-to-end batch ETL pipeline using Python and PostgreSQL with the Olist Brazilian E-Commerce dataset. The pipeline extracts nine related CSV datasets, validates the source data, applies dataset-specific transformations, performs data-quality validation, and bulk loads the processed data into PostgreSQL using COPY. I designed the database with primary keys, composite keys, and foreign-key relationships, then added database-level validation to check row counts, keys, and orphan records. I also implemented orchestration, logging, failure handling, and repeatable full-refresh loading. One important part of the project was investigating data-quality issues rather than blindly removing duplicates, such as repeated review identifiers and repeated geolocation ZIP prefixes.

---

# 17. Key Takeaways

This project demonstrates practical ETL concepts including:

- Source data profiling
- Data-quality analysis
- Null handling
- Duplicate investigation
- Primary keys
- Composite keys
- Foreign keys
- Data type standardization
- Text normalization
- Relational schema design
- PostgreSQL bulk loading
- Full-refresh ETL
- Pipeline orchestration
- Logging
- Error handling
- Repeatability
- End-to-end validation

The main objective is to demonstrate the construction of a reliable and end-to-end ETL pipeline from raw source files to a validated relational database.