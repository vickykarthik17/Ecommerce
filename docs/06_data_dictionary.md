# E-Commerce ETL Pipeline
# Data Dictionary and Project Progress

## 1. Project Overview

**Project:** E-Commerce End-to-End ETL Pipeline  
**Dataset:** Olist E-Commerce Dataset  
**Project Goal:** Build an end-to-end ETL pipeline that extracts raw data, cleans and transforms it, stores the processed data in PostgreSQL, and makes the pipeline ready for further use.

**Current stage:** Sprint 1  
**Current date:** August 11, 2026

---

# 2. Sprint Plan

| Sprint | Dates | Main Work |
|---|---|---|
| Sprint 1 | Aug 10 - Aug 13 | Requirements + Extraction |
| Sprint 2 | Aug 14 - Aug 17 | Cleaning + Transformation |
| Sprint 3 | Aug 18 - Aug 21 | PostgreSQL + Data Loading |
| Sprint 4 | Aug 22 - Aug 24 | Automation + Testing |
| Final Release | Aug 25 | Documentation + Final Project |

---

# 3. Daily Project Progress

## August 10, 2026

**Sprint:** Sprint 1  
**Focus:** Understanding and profiling the source data

### Completed

- Reviewed all 9 source CSV files.
- Checked the number of rows and columns in each dataset.
- Checked data types.
- Checked missing values.
- Checked duplicate records.
- Checked possible primary keys.
- Checked relationships between datasets.
- Checked for orphan records.
- Investigated duplicate review IDs and order IDs.
- Investigated duplicate records in the Geolocation dataset.
- Identified exact duplicate Geolocation rows.
- Created the initial Data Dictionary.

### Important findings

- Most datasets have clean primary identifier columns.
- Reviews contain repeated `review_id` and `order_id` values.
- The combination `review_id + order_id` is unique in the Reviews dataset.
- Geolocation contains many repeated ZIP prefixes.
- Geolocation contains 261,836 exact duplicate rows.
- Some datasets contain missing values that will need to be handled during transformation.
- No orphan records were found in the tested relationships.

---

## August 11, 2026

**Sprint:** Sprint 1  
**Focus:** Building the extraction layer

### Completed

Created the extraction folder:

```text
src/
└── extraction/
    ├── extract_data.py
    ├── expected_columns.py
    └── validate_data.py
```

### What the extraction layer does

The extraction process:

```text
Raw CSV files
     ↓
Check file exists
     ↓
Read CSV using Pandas
     ↓
Check dataset is not empty
     ↓
Check expected columns
     ↓
Valid dataset
```

### Validation result

All 9 datasets successfully passed extraction validation:

```text
olist_customers_dataset.csv: 99441 rows, 5 columns, Valid
olist_geolocation_dataset.csv: 1000163 rows, 5 columns, Valid
olist_order_items_dataset.csv: 112650 rows, 7 columns, Valid
olist_order_payments_dataset.csv: 103886 rows, 5 columns, Valid
olist_order_reviews_dataset.csv: 99224 rows, 7 columns, Valid
olist_orders_dataset.csv: 99441 rows, 8 columns, Valid
olist_products_dataset.csv: 32951 rows, 9 columns, Valid
olist_sellers_dataset.csv: 3095 rows, 4 columns, Valid
product_category_name_translation.csv: 71 rows, 2 columns, Valid
```

### Not done yet

Logging was discussed but intentionally not implemented yet.

---

# 4. Source Dataset Summary

The project currently uses 9 source datasets.

| Dataset | Rows | Columns | Main Purpose |
|---|---:|---:|---|
| Customers | 99,441 | 5 | Customer information |
| Geolocation | 1,000,163 | 5 | Geographic information |
| Order Items | 112,650 | 7 | Products included in orders |
| Order Payments | 103,886 | 5 | Payment information |
| Order Reviews | 99,224 | 7 | Customer reviews |
| Orders | 99,441 | 8 | Order information |
| Products | 32,951 | 9 | Product information |
| Sellers | 3,095 | 4 | Seller information |
| Category Translation | 71 | 2 | Product category translation |

---

# 5. Customers

**File:** `olist_customers_dataset.csv`  
**Rows:** 99,441  
**Columns:** 5  
**Main purpose:** Stores customer information.

### Columns

- `customer_id`: ID used to connect a customer with an order.
- `customer_unique_id`: Unique identifier for the customer.
- `customer_zip_code_prefix`: Customer ZIP code prefix.
- `customer_city`: Customer city.
- `customer_state`: Customer state.

### Key findings

- `customer_id`: No nulls and no duplicates.
- `customer_unique_id`: 3,345 duplicate values.
- No null values were found in the dataset.

### Relationship

```text
customers.customer_id
        ↓
orders.customer_id
```

**Orphan records:** 0

### Future transformation

- Validate ZIP codes.
- Standardize city and state values if required.
- Keep both customer IDs.

---

# 6. Orders

**File:** `olist_orders_dataset.csv`  
**Rows:** 99,441  
**Columns:** 8  
**Main purpose:** Stores information about customer orders.

### Columns

- `order_id`: Unique ID of the order.
- `customer_id`: ID of the customer who placed the order.
- `order_status`: Current order status.
- `order_purchase_timestamp`: Time when the order was placed.
- `order_approved_at`: Time when the order was approved.
- `order_delivered_carrier_date`: Date when the order was handed to the carrier.
- `order_delivered_customer_date`: Date when the order reached the customer.
- `order_estimated_delivery_date`: Estimated delivery date.

### Key findings

- `order_id`: No nulls and no duplicates.
- `order_approved_at`: 160 null values.
- `order_delivered_carrier_date`: 1,783 null values.
- `order_delivered_customer_date`: 2,965 null values.

These missing dates should not automatically be replaced because they may have a valid meaning depending on the order status.

### Relationships

```text
orders.customer_id
        ↓
customers.customer_id

orders.order_id
        ↓
order_items.order_id

orders.order_id
        ↓
order_payments.order_id

orders.order_id
        ↓
order_reviews.order_id
```

**Orphan records:** 0 in the tested relationships.

### Future transformation

- Convert date columns from text to datetime.
- Handle missing dates carefully.
- Validate order status values.

---

# 7. Order Items

**File:** `olist_order_items_dataset.csv`  
**Rows:** 112,650  
**Columns:** 7  
**Main purpose:** Stores the products included in each order.

### Columns

- `order_id`: Order ID.
- `order_item_id`: Item number within the order.
- `product_id`: Product ID.
- `seller_id`: Seller ID.
- `shipping_limit_date`: Latest date by which the item should be shipped.
- `price`: Product price.
- `freight_value`: Shipping cost.

### Key findings

- No null values.
- No duplicate records.
- `order_id` alone is not unique because an order can contain multiple products.
- `order_id + order_item_id` can be used as a composite key.

### Relationships

```text
order_items.order_id
        ↓
orders.order_id

order_items.product_id
        ↓
products.product_id

order_items.seller_id
        ↓
sellers.seller_id
```

**Orphan records:** 0

### Future transformation

- Convert `shipping_limit_date` to datetime.
- Validate price and freight values.
- Keep the composite key.

---

# 8. Order Payments

**File:** `olist_order_payments_dataset.csv`  
**Rows:** 103,886  
**Columns:** 5  
**Main purpose:** Stores payment information for orders.

### Columns

- `order_id`: Order ID.
- `payment_sequential`: Payment sequence number.
- `payment_type`: Payment method.
- `payment_installments`: Number of installments.
- `payment_value`: Payment amount.

### Key findings

- No null values.
- No duplicate records.
- One order can have multiple payment records.
- `order_id + payment_sequential` can be used as a composite key.

### Relationship

```text
order_payments.order_id
        ↓
orders.order_id
```

**Orphan records:** 0

### Future transformation

- Validate payment amounts.
- Validate installment values.
- Standardize payment types if required.

---

# 9. Order Reviews

**File:** `olist_order_reviews_dataset.csv`  
**Rows:** 99,224  
**Columns:** 7  
**Main purpose:** Stores customer review information.

### Columns

- `review_id`: Review ID.
- `order_id`: Order ID connected to the review.
- `review_score`: Customer rating.
- `review_comment_title`: Review title.
- `review_comment_message`: Review message.
- `review_creation_date`: Date when the review was created.
- `review_answer_timestamp`: Time when the review was answered.

### Key findings

- `review_id`: 814 duplicate values.
- `order_id`: 551 duplicate values.
- `review_id + order_id`: No duplicate combinations.
- `review_comment_title`: 87,656 null values.
- `review_comment_message`: 58,247 null values.

### Important investigation

We investigated the repeated review IDs instead of simply deleting them.

The investigation showed that a repeated `review_id` can be associated with different orders.

Therefore:

```text
Do not remove a row just because review_id is repeated.
```

For now, `review_id + order_id` is treated as the candidate composite key.

### Relationship

```text
order_reviews.order_id
        ↓
orders.order_id
```

**Orphan records:** 0

### Future transformation

- Convert date fields to datetime.
- Keep valid missing review comments.
- Validate review scores.
- Re-check the composite key.

---

# 10. Products

**File:** `olist_products_dataset.csv`  
**Rows:** 32,951  
**Columns:** 9  
**Main purpose:** Stores product information.

### Columns

- `product_id`: Product ID.
- `product_category_name`: Product category.
- `product_name_lenght`: Length of product name.
- `product_description_lenght`: Length of product description.
- `product_photos_qty`: Number of product photos.
- `product_weight_g`: Product weight in grams.
- `product_length_cm`: Product length in centimeters.
- `product_height_cm`: Product height in centimeters.
- `product_width_cm`: Product width in centimeters.

### Key findings

- `product_id`: No nulls and no duplicates.
- `product_category_name`: 610 null values.
- `product_name_lenght`: 610 null values.
- `product_description_lenght`: 610 null values.
- `product_photos_qty`: 610 null values.
- Weight and dimension fields contain 2 null values each.

### Relationship

```text
products.product_id
        ↓
order_items.product_id
```

**Orphan records:** 0

### Future transformation

- Handle missing product information.
- Validate numeric product fields.
- Join category translation data.

---

# 11. Sellers

**File:** `olist_sellers_dataset.csv`  
**Rows:** 3,095  
**Columns:** 4  
**Main purpose:** Stores seller information.

### Columns

- `seller_id`: Seller ID.
- `seller_zip_code_prefix`: Seller ZIP code prefix.
- `seller_city`: Seller city.
- `seller_state`: Seller state.

### Key findings

- No null values.
- No duplicate seller IDs.
- `seller_id` can be used as the candidate primary key.

### Relationship

```text
sellers.seller_id
        ↓
order_items.seller_id
```

**Orphan records:** 0

### Future transformation

- Validate ZIP codes.
- Standardize city and state values if needed.

---

# 12. Geolocation

**File:** `olist_geolocation_dataset.csv`  
**Rows:** 1,000,163  
**Columns:** 5  
**Main purpose:** Stores geographic information for ZIP code prefixes.

### Columns

- `geolocation_zip_code_prefix`: ZIP code prefix.
- `geolocation_lat`: Latitude.
- `geolocation_lng`: Longitude.
- `geolocation_city`: City.
- `geolocation_state`: State.

### Key findings

- Unique ZIP prefixes: 19,015.
- ZIP prefixes with multiple records: 17,972.
- ZIP prefix is not unique.
- Exact duplicate rows: 261,836.
- Rows remaining after removing exact duplicates: 738,327.

### Important investigation

We checked ZIP prefix `24220`.

Multiple records had:

- The same ZIP prefix.
- The same city/state.
- Different latitude and longitude values.

This means repeated ZIP prefixes are not automatically bad data.

### Transformation decision

```text
Exact duplicate row
        ↓
Can be removed

Same ZIP prefix + different location
        ↓
Keep unless another business rule says otherwise
```

### Important rule

Do not use `geolocation_zip_code_prefix` alone as a primary key.

### Future transformation

- Remove exact duplicate rows.
- Preserve valid geographic observations.
- Validate latitude and longitude.
- Standardize city names if needed.

---

# 13. Category Translation

**File:** `product_category_name_translation.csv`  
**Rows:** 71  
**Columns:** 2  
**Main purpose:** Provides English translations for product categories.

### Columns

- `product_category_name`: Original category name.
- `product_category_name_english`: English category name.

### Key findings

- No null values.
- No duplicate category names.
- `product_category_name` can be used as a candidate key.

### Future transformation

- Use this dataset to translate product categories.
- Keep the original category name.
- Add the English category where a translation is available.

---

# 14. Relationship Checks

The following relationships were tested:

| Parent | Child | Key | Orphan Records |
|---|---|---|---:|
| Customers | Orders | `customer_id` | 0 |
| Orders | Order Items | `order_id` | 0 |
| Products | Order Items | `product_id` | 0 |
| Sellers | Order Items | `seller_id` | 0 |
| Orders | Payments | `order_id` | 0 |
| Orders | Reviews | `order_id` | 0 |

### Meaning of an orphan record

An orphan record is a child record that refers to a parent ID that does not exist.

Example:

```text
Order Items
order_id = ABC123
       ↓
Orders
order_id = ABC123
```

This is valid.

If `ABC123` does not exist in Orders, the Order Item would be an orphan record.

No orphan records were found in our tested relationships.

---

# 15. Main Data Quality Findings

These are the main issues identified so far:

### Customers

- `customer_unique_id` has 3,345 duplicate values.

### Orders

- Some approval and delivery dates are missing.

### Reviews

- `review_id` has 814 duplicate values.
- `order_id` has 551 duplicate values.
- Review title and message contain many null values.
- `review_id + order_id` is currently unique.

### Products

- Several product attributes contain missing values.
- 610 products have missing category/name-related attributes.
- Weight and dimension fields have 2 missing values each.

### Geolocation

- 261,836 exact duplicate rows.
- ZIP prefix is not unique.
- Multiple valid geographic observations can exist for one ZIP prefix.

### Relationships

- No orphan records were found in the tested relationships.

---

# 16. Current ETL Architecture

The project is being developed as an end-to-end ETL pipeline.

Current architecture:

```text
                 RAW DATA
                    │
                    ▼
              data/raw/*.csv
                    │
                    ▼
             EXTRACTION
                    │
                    ▼
          Basic Validation
          ├── File exists
          ├── Not empty
          └── Expected columns
                    │
                    ▼
          TRANSFORMATION
             (Next stage)
                    │
                    ▼
             PostgreSQL
             (Later stage)
                    │
                    ▼
          Final ETL Pipeline
```

---

# 17. Current Project Status

## Sprint 1: Aug 10 - Aug 13

**Goal:** Requirements + Extraction

### Completed

- Source data understanding
- Source profiling
- Null analysis
- Duplicate analysis
- Key analysis
- Relationship analysis
- Orphan-record checks
- Review investigation
- Geolocation investigation
- Data Dictionary
- Extraction script
- Expected column validation
- Empty dataset validation
- File existence validation
- Extraction testing

### Pending

- Additional extraction testing
- Extraction logging
- Any remaining Sprint 1 tasks

---

## Sprint 2: Aug 14 - Aug 17

**Goal:** Cleaning + Transformation

Planned work:

- Handle duplicates according to documented rules.
- Handle missing values.
- Convert data types.
- Convert date and timestamp columns.
- Standardize text fields.
- Create cleaned/curated datasets.
- Apply business rules identified during profiling.

---

## Sprint 3: Aug 18 - Aug 21

**Goal:** PostgreSQL + Data Loading

Planned work:

- Design target database tables.
- Define primary keys.
- Define foreign keys.
- Define appropriate PostgreSQL data types.
- Create tables.
- Load transformed datasets.
- Validate loaded row counts and relationships.

---

## Sprint 4: Aug 22 - Aug 24

**Goal:** Automation + Testing

Planned work:

- Connect the ETL stages.
- Automate the pipeline.
- Add required logging.
- Test the complete pipeline.
- Handle pipeline failures.
- Validate final data quality.

---

## Final Release: Aug 25

**Goal:** Complete Project

Planned work:

- Final testing.
- Final documentation.
- Project architecture documentation.
- Setup instructions.
- Final ETL workflow documentation.
- Final project demonstration.

---

# 18. Current Files

The important project files created so far are:

```text
Ecommerce/
│
├── data/
│   └── raw/
│
├── docs/
│   └── 06_data_dictionary.md
│
└── src/
    ├── profiling/
    │   ├── profile_sources.py
    │   ├── analyse_keys.py
    │   ├── analyse_relationships.py
    │   └── investigate/
    │       ├── investigate_reviews.py
    │       └── investigate_geolocation.py
    │
    └── extraction/
        ├── extract_data.py
        ├── expected_columns.py
        └── validate_data.py
```

---

# 19. Important Note

The raw datasets are being treated as the source layer.

We should **not modify the files inside `data/raw/`**.

All cleaning and transformation should happen in the next ETL stages.

This keeps the pipeline reproducible:

```text
Raw Data
   ↓
Extract
   ↓
Transform
   ↓
Load
```

If a transformation rule changes later, we can run the pipeline again from the original raw data.
