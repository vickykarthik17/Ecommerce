1. Project Overview

Project: E-Commerce End-to-End ETL Pipeline
Dataset: Olist E-Commerce Dataset
Project goal: Build an end-to-end ETL pipeline that extracts raw data, cleans and transforms it, stores processed data in PostgreSQL, and makes the pipeline ready for further use.
Current stage: Sprint 3
Current date: August 18, 2026

2. Sprint Plan

1. Sprint 1 (Aug 10 - Aug 13): Requirements and extraction
2. Sprint 2 (Aug 14 - Aug 17): Cleaning and transformation
3. Sprint 3 (Aug 18 - Aug 21): PostgreSQL and data loading
4. Sprint 4 (Aug 22 - Aug 24): Automation and testing
5. Final Release (Aug 25): Documentation and final project

3. Daily Project Progress

3.1 August 10, 2026
Focus: Understanding and profiling the source data
Completed: Reviewed all nine source CSV files, checked row and column counts, reviewed data types, missing values, duplicates, candidate keys, dataset relationships, orphan records, duplicate review IDs and order IDs, duplicate geolocation rows, and created the initial data dictionary.
Important findings: Most datasets have clean identifier columns. Reviews have repeated review_id and order_id values, but the combination of review_id and order_id is unique. Geolocation has many repeated ZIP prefixes and 261,836 exact duplicate rows. Some datasets contain missing values that will need handling during transformation. No orphan records were found in the tested relationships.

3.2 August 11, 2026
Focus: Building the extraction layer
Completed: Created the extraction module with extract_data.py, expected_columns.py, and validate_data.py. The extraction process now reads raw CSV files, checks that each file exists, ensures datasets are not empty, validates expected columns, and marks datasets as valid.
Validation result: All nine datasets passed extraction validation. The counts and columns were confirmed, and each source file was marked valid.
Not done yet: Extraction logging was discussed but not implemented.

3.3 August 18, 2026
Focus: PostgreSQL database setup, data loading, and validation
Completed:
- Installed and configured PostgreSQL 18.
- Created the ecommerce PostgreSQL database.
- Created the PostgreSQL schema with 9 tables and defined primary and foreign-key relationships.
- Configured Python database connectivity using psycopg and environment variables.
- Successfully tested the Python to PostgreSQL connection.
- Loaded all 9 processed Olist datasets into PostgreSQL.
- Used a separate bulk loading script for the large geolocation dataset containing 738,327 rows.
- Verified that PostgreSQL row counts match the processed datasets.
- Validated foreign-key relationships across the database.
- All orphan-record checks returned zero results.

Data Loaded:

| Table | Rows |
|---|---:|
| customers | 99,441 |
| orders | 99,441 |
| order_items | 112,650 |
| payments | 103,886 |
| reviews | 99,224 |
| products | 32,951 |
| sellers | 3,095 |
| geolocation | 738,327 |
| category_translation | 71 |

Blockers and Resolutions:

1. Timestamp datatype mismatch during order loading

   PostgreSQL rejected missing datetime values because Pandas represented them as NaN, which PostgreSQL interpreted as a numeric value instead of NULL.

   Resolution: Converted Pandas missing values to Python None before loading:

   data = data.astype(object).where(pd.notna(data), None)

   Orders were then loaded successfully.

2. Duplicate primary-key error during product loading

   The products dataset was accidentally loaded more than once, causing a duplicate product_id error.

   Resolution: Avoided rerunning datasets that had already been loaded. The issue also highlighted the need to make the final loading process safe for repeated execution.

3. Large geolocation dataset

   The geolocation dataset contains 738,327 rows, making row-by-row insertion inefficient.

   Resolution: Created a separate load_geolocation.py script using PostgreSQL bulk COPY loading.

Validation Result:

- Row-count validation: Passed
- Foreign-key validation: Passed
- Orphan-record checks: Passed
- All 9 datasets successfully loaded into PostgreSQL.

Sprint 3 Progress:

PostgreSQL database setup and data loading are complete. Initial database integrity validation has also been completed successfully.

Next Steps:

- Validate primary and composite keys in PostgreSQL.
- Complete database validation.
- Improve the loading process for safe reruns.
- Commit and push the PostgreSQL loading work.
- Continue with the remaining Sprint 3 tasks.

4. Source Dataset Summary

The project uses nine source datasets.
1. Customers: 99,441 rows, 5 columns
2. Geolocation: 1,000,163 rows, 5 columns
3. Order Items: 112,650 rows, 7 columns
4. Order Payments: 103,886 rows, 5 columns
5. Order Reviews: 99,224 rows, 7 columns
6. Orders: 99,441 rows, 8 columns
7. Products: 32,951 rows, 9 columns
8. Sellers: 3,095 rows, 4 columns
9. Category Translation: 71 rows, 2 columns

5. Customers

File: olist_customers_dataset.csv
Rows: 99,441
Columns: 5
Main purpose: Stores customer information.
Columns: customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state.
Key findings: customer_id is clean with no nulls and no duplicates. customer_unique_id has 3,345 duplicate values. The dataset has no null values overall.
Relationship: customers.customer_id maps to orders.customer_id.
Orphan records: 0.
Future transformation: Validate ZIP codes, standardize city and state values if needed, keep both customer identifiers.

6. Orders

File: olist_orders_dataset.csv
Rows: 99,441
Columns: 8
Main purpose: Stores information about customer orders.
Columns: order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date.
Key findings: order_id is clean. There are 160 null values in order_approved_at, 1,783 null values in order_delivered_carrier_date, and 2,965 null values in order_delivered_customer_date. These missing dates should not be replaced automatically because they can reflect valid order status conditions.
Relationships: orders.customer_id maps to customers.customer_id; orders.order_id maps to order_items.order_id, order_payments.order_id, order_reviews.order_id.
Orphan records: 0.
Future transformation: Convert date columns to datetime, handle missing dates carefully, validate order status values.

7. Order Items

File: olist_order_items_dataset.csv
Rows: 112,650
Columns: 7
Main purpose: Stores the products included in each order.
Columns: order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value.
Key findings: No null values and no duplicate rows. order_id is not unique by itself because each order can have multiple items. order_id and order_item_id together form a composite key.
Relationships: order_items.order_id maps to orders.order_id; order_items.product_id maps to products.product_id; order_items.seller_id maps to sellers.seller_id.
Orphan records: 0.
Future transformation: Convert shipping_limit_date to datetime, validate price and freight values, preserve the composite key.

8. Order Payments

File: olist_order_payments_dataset.csv
Rows: 103,886
Columns: 5
Main purpose: Stores payment information for orders.
Columns: order_id, payment_sequential, payment_type, payment_installments, payment_value.
Key findings: No null values and no duplicate rows. One order can have multiple payment records. order_id and payment_sequential can form a composite key.
Relationship: order_payments.order_id maps to orders.order_id.
Orphan records: 0.
Future transformation: Validate payment amounts, validate installment values, standardize payment types if needed.

9. Order Reviews

File: olist_order_reviews_dataset.csv
Rows: 99,224
Columns: 7
Main purpose: Stores customer review information.
Columns: review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp.
Key findings: review_id has 814 duplicate values, order_id has 551 duplicate values, and review_id plus order_id is unique. review_comment_title has 87,656 null values, and review_comment_message has 58,247 null values.
Important investigation: Repeated review_id values were reviewed rather than deleted. The same review_id can appear for different orders, so rows should not be removed solely because review_id is repeated. The candidate composite key is review_id plus order_id.
Relationship: order_reviews.order_id maps to orders.order_id.
Orphan records: 0.
Future transformation: Convert review dates to datetime, keep valid missing review comments, validate review scores, re-check the composite key.

10. Products

File: olist_products_dataset.csv
Rows: 32,951
Columns: 9
Main purpose: Stores product information.
Columns: product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm.
Key findings: product_id is clean. There are 610 missing values in category, name length, description length, and photo quantity. Weight and dimension fields each have 2 missing values.
Relationship: products.product_id maps to order_items.product_id.
Orphan records: 0.
Future transformation: Handle missing product details, validate numeric fields, join category translation data.

11. Sellers

File: olist_sellers_dataset.csv
Rows: 3,095
Columns: 4
Main purpose: Stores seller information.
Columns: seller_id, seller_zip_code_prefix, seller_city, seller_state.
Key findings: No null values and no duplicate seller IDs. seller_id is a good candidate for the primary key.
Relationship: sellers.seller_id maps to order_items.seller_id.
Orphan records: 0.
Future transformation: Validate ZIP codes, standardize city and state values if needed.

12. Geolocation

File: olist_geolocation_dataset.csv
Rows: 1,000,163
Columns: 5
Main purpose: Stores geographic information for ZIP code prefixes.
Columns: geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state.
Key findings: There are 19,015 unique ZIP prefixes. Most ZIP prefixes appear in multiple rows. Exact duplicate rows total 261,836, leaving 738,327 rows after removing exact duplicates.
Investigation: For ZIP prefix 24220, multiple rows had the same city and state but different latitude and longitude values. That means repeated ZIP prefixes can be valid and should not be treated as bad data by default.
Transformation decision: Remove exact duplicate rows, keep distinct rows with the same ZIP prefix if they represent valid geographic observations, do not use geolocation_zip_code_prefix alone as a primary key.
Future transformation: Remove exact duplicate rows, preserve valid geographic observations, validate latitude and longitude, standardize city names if needed.

13. Category Translation

File: product_category_name_translation.csv
Rows: 71
Columns: 2
Main purpose: Provides English translations for product categories.
Columns: product_category_name, product_category_name_english.
Key findings: No null values and no duplicate category names. product_category_name can be a candidate key.
Future transformation: Use this dataset to translate product categories, keep the original category name, add English translations where available.

14. Relationship Checks

Tested relationships: Customers to Orders using customer_id; Orders to Order Items using order_id; Products to Order Items using product_id; Sellers to Order Items using seller_id; Orders to Payments using order_id; Orders to Reviews using order_id.
No orphan child records were found in the tested relationships.

15. Main Data Quality Findings

Customers: customer_unique_id has 3,345 duplicate values.
Orders: Some approval and delivery dates are missing.
Reviews: review_id has 814 duplicate values, order_id has 551 duplicate values, review titles and messages contain many null values, and review_id plus order_id is unique.
Products: Several product fields have missing values, including category, name length, description length, and photo quantity. Weight and dimensions have 2 missing values each.
Geolocation: There are 261,836 exact duplicate rows, and ZIP prefix is not unique. Multiple valid geographic observations can exist for one ZIP prefix.
Relationships: No orphan records were found in the tested relationships.

16. Current ETL Architecture

The ETL pipeline is being built as raw data in data/raw/*.csv, then extraction, then transformation, and later PostgreSQL loading. The current extraction step validates file existence, checks that each dataset is not empty, and verifies expected columns.

17. Current Project Status

Sprint 1 (Aug 10 - Aug 13): Requirements and extraction.
Completed: Source data understanding, profiling, null and duplicate analysis, key and relationship checks, review and geolocation investigations, data dictionary creation, extraction scripting, expected schema validation, empty dataset validation, file existence validation, extraction testing.
Pending: Additional extraction testing, extraction logging, remaining Sprint 1 tasks.

Sprint 2 (Aug 14 - Aug 17): Cleaning and transformation.
Planned work: Handle duplicates, handle missing values, convert data types, convert date and timestamp columns, standardize text fields, create cleaned datasets, apply business rules.

Sprint 3 (Aug 18 - Aug 21): PostgreSQL and data loading.
Completed: PostgreSQL 18 was installed and configured, the ecommerce database and schema were created, all nine processed datasets were loaded into PostgreSQL, row counts were validated, foreign keys were checked, and orphan-record validation returned zero results.
Remaining work: Validate primary and composite keys in PostgreSQL, improve the loading process for safe reruns, and finalize the database validation checklist.

Sprint 4 (Aug 22 - Aug 24): Automation and testing.
Planned work: Connect ETL stages, automate the pipeline, add logging, test the complete pipeline, handle failures, validate final data quality.

Final Release (Aug 25): Complete project.
Planned work: Final testing, final documentation, architecture documentation, setup instructions, ETL workflow documentation, project demonstration.

18. Current Files

The main project files are in the source, data, and docs folders. The extraction code is under src/extraction, and profiling scripts are under src/profiling.

19. Important Note

The raw datasets in data/raw are the source layer and should not be modified. All cleaning and transformation will happen in later ETL stages so the pipeline stays reproducible from the original raw data.

20. August 12, 2026 Update

Sprint 1 focus: Extraction refinement and validation.
Completed: Refined extraction for all source datasets, added expected schema validation, file existence validation, empty dataset validation, CSV read-error handling, confirmed all nine datasets were successfully extracted and validated.
Validation result: All source files were valid.
Sprint 1 progress: Extraction and basic source validation are complete. The extraction layer is ready for the final Sprint 1 review and source-to-target mapping.


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

The project is implemented as an end-to-end ETL pipeline. Each stage runs from the project root, uses the same Python interpreter through `sys.executable`, and stops the pipeline when a stage fails.

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
       Dataset-specific cleaning
       and data-quality validation
                    │
                    ▼
          PostgreSQL full refresh
       TRUNCATE ... CASCADE + COPY
                    │
                    ▼
          Database validation
       Counts, keys, and foreign keys
```

The orchestration entry point is `src/run_pipeline.py`. Its execution order is:

1. Extract the raw source files.
2. Validate source file existence, contents, and expected columns.
3. Transform customers, orders, order items, payments, reviews, products, sellers, geolocation, and category translation.
4. Validate all processed datasets.
5. Reset the PostgreSQL target tables and bulk-load the processed datasets with `COPY`.
6. Load the large geolocation dataset through its dedicated loader.
7. Validate database row counts, primary keys, composite keys, and foreign-key relationships.

The raw files in `data/raw/` remain unchanged. Processed files are written to `data/processed/`, which provides a clear source-to-target boundary and allows the complete pipeline to be rerun from the original inputs.

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

- Structured extraction logging is still a future improvement.
- Additional automated end-to-end tests are still planned.

---

## Sprint 2: Aug 14 - Aug 17

**Goal:** Cleaning + Transformation

Completed:

- Transformed all nine datasets into `data/processed/`.
- Applied the documented rules for missing values, duplicate rows, identifiers, text fields, and date columns.
- Renamed the misspelled source product columns to `product_name_length` and `product_description_length`.
- Removed only exact duplicate geolocation rows while preserving valid repeated ZIP-prefix observations.
- Validated the processed datasets with the transformation validation scripts.

Outcome: All nine processed datasets passed the current transformation and data-quality checks.

---

## Sprint 3: Aug 18 - Aug 21

**Goal:** PostgreSQL + Data Loading

Completed:

- Configured PostgreSQL 18 and created the `ecommerce` database.
- Created the relational schema for all nine processed datasets.
- Defined primary keys, composite keys, and foreign keys based on source profiling.
- Configured the Python connection with the PostgreSQL `dbname` parameter.
- Replaced row-by-row inserts with PostgreSQL `COPY` bulk loading.
- Implemented full-refresh loading with `TRUNCATE ... CASCADE` before each complete batch load.
- Loaded all processed datasets and validated row counts, keys, and foreign-key relationships.

Outcome: The database contains the complete processed dataset and can be safely reloaded by rerunning the full batch pipeline.

---

## Sprint 4: Aug 22 - Aug 24

**Goal:** Automation + Testing

Completed:

- Connected extraction, validation, transformation, loading, and database validation in `src/run_pipeline.py`.
- Configured the orchestrator to stop immediately when a stage returns a failure code.
- Executed a successful end-to-end pipeline run.
- Verified that the final database matched the processed dataset sizes and relationship rules.

Remaining work:

- Add structured logging and clearer failure summaries.
- Expand automated end-to-end test coverage.
- Improve pipeline observability.

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

The core ETL pipeline is operational. The remaining release work is focused on documentation cleanup, repeatable testing, structured logging, and observability rather than on completing the core extraction, transformation, or database-loading path.

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

### August 12, 2026

**Sprint:** 1
**Focus:** Extraction Refinement and Validation

**Completed:**

* Refined the data extraction process for all source datasets.
* Integrated expected schema validation with the extraction process.
* Added file existence validation to identify missing source files.
* Added empty dataset validation to prevent empty files from being processed.
* Added CSV read-error handling so the pipeline can continue if a file cannot be read.
* Confirmed that all 9 source datasets were successfully extracted and validated.
* Verified that all 9 datasets returned a **Valid** status.

**Validation Result:**

* `olist_customers_dataset.csv`: Valid
* `olist_geolocation_dataset.csv`: Valid
* `olist_order_items_dataset.csv`: Valid
* `olist_order_payments_dataset.csv`: Valid
* `olist_order_reviews_dataset.csv`: Valid
* `olist_orders_dataset.csv`: Valid
* `olist_products_dataset.csv`: Valid
* `olist_sellers_dataset.csv`: Valid
* `product_category_name_translation.csv`: Valid

**Sprint 1 Progress:**
Extraction and basic source validation are complete. The extraction layer is ready for the final Sprint 1 review and source-to-target mapping.

---

### August 16, 2026

**Sprint:** 2
**Focus:** Transformation Finalization and Data Quality Validation

**Completed:**

* Completed transformation of all 9 Olist datasets.
* Created processed datasets in `data/processed/`.
* Standardized identifiers, text fields, and date columns where required.
* Preserved meaningful null values instead of removing them blindly.
* Corrected inconsistent product column names during transformation.
* Removed only exact duplicate rows from the geolocation dataset.
* Preserved repeated geolocation ZIP prefixes because they can represent valid geographic records.
* Validated business keys and duplicate records across the processed datasets.
* Completed overall data-quality validation.
* Updated transformation rules in `docs/07_transformation_rules.md`.

**Validation Result:**

All 9 processed datasets passed the current transformation and data-quality checks.

**Sprint 2 Progress:**

Transformation and validation are complete. The processed datasets are ready for PostgreSQL schema design and loading.

**Next Steps:**

Prepare the PostgreSQL target schema, including table structure, primary keys, foreign keys, and data type mapping.

---

# 20. Implementation Progress: August 19-20, 2026

This section records the database and orchestration decisions that changed the ETL pipeline from a collection of working scripts into a repeatable end-to-end process. It complements the dataset definitions above by explaining how the processed data is validated and delivered to PostgreSQL.

## August 19, 2026: PostgreSQL Setup, Loading, and Validation

### Completed

- Configured PostgreSQL 18 as the target database.
- Created the `ecommerce` database and relational schema for all nine processed datasets.
- Defined primary keys, composite keys, and foreign keys from the profiling results.
- Tested Python-to-PostgreSQL connectivity with `psycopg` and environment-based configuration.
- Replaced individual `INSERT` statements with PostgreSQL `COPY` bulk loading.
- Loaded the processed datasets and validated row counts, keys, and foreign-key relationships.
- Loaded geolocation separately because its processed size is 738,327 rows.

### Blockers and resolutions

| Blocker | Cause | Resolution |
|---|---|---|
| PostgreSQL connection failure | The connection configuration used `database`, which PostgreSQL does not accept as the database-name option. | Changed the configuration to use `dbname`. The connection test then passed. |
| Inefficient loading approach | Individual `INSERT` operations would require too many database operations for the larger datasets. | Replaced row-by-row inserts with PostgreSQL `COPY` bulk loading. |
| Product loading failure | Pandas wrote integer product attributes as values such as `40.0`, but PostgreSQL expected integer text. | Converted `product_name_length`, `product_description_length`, and `product_photos_qty` to integer strings while preserving missing values as blanks for PostgreSQL `NULL` handling. |
| Large geolocation load | The processed geolocation dataset contains 738,327 rows. | Used the dedicated geolocation loader with bulk `COPY`. |

## August 20, 2026: Orchestration and Repeat-Safe Loading

### Pipeline execution order

The orchestration script `src/run_pipeline.py` runs the stages in a fixed order:

```text
Extract source data
   |
Validate source data
   |
Transform nine datasets
   |
Validate processed datasets
   |
Reset PostgreSQL tables
   |
Bulk-load processed datasets
   |
Load geolocation
   |
Validate the database
```

Each stage is executed with `subprocess.run()` and `sys.executable`. A non-zero exit code stops the pipeline and identifies the failed stage, preventing later stages from running against incomplete data.

### Repeat-safe full-refresh loading

The first end-to-end run failed during loading because the database still contained records from an earlier loading test. PostgreSQL correctly rejected the second load with a duplicate primary-key error for `customer_id = 06b8999e2fba1a1fbc88172c00ba8bc7`.

The loading stage now uses PostgreSQL full-refresh loading and resets the destination before loading a complete batch:

```text
TRUNCATE TABLE ... CASCADE
   |
   ▼
COPY processed CSV files into PostgreSQL
```

This full-refresh strategy is appropriate because every run processes the complete source dataset. It removes stale rows, avoids duplicate-key conflicts on reruns, and makes the pipeline repeatable without manual database cleanup.

### Successful end-to-end result

The complete pipeline passed extraction, source validation, all nine transformations, processed-data validation, PostgreSQL reset, bulk loading, geolocation loading, and database validation.

| Dataset | Final database rows |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Payments | 103,886 |
| Reviews | 99,224 |
| Products | 32,951 |
| Sellers | 3,095 |
| Geolocation | 738,327 |
| Category Translation | 71 |

### Final validation outcome

- All applicable primary-key and composite-key checks passed.
- All configured foreign-key checks passed.
- Orphan-record checks returned zero results for Orders to Customers, Order Items to Orders, Order Items to Products, Order Items to Sellers, Payments to Orders, and Reviews to Orders.
- The geolocation transformation produced 738,327 rows after exact duplicate removal. Its status output was corrected to report the row count without an extra blank value.

## Current Focus

The core ETL pipeline is operational. The next improvements are structured logging, clearer failure reporting, stronger end-to-end test coverage, and improved observability. These additions will make failures easier to diagnose while preserving the current extraction, transformation, validation, and full-refresh loading behavior.
