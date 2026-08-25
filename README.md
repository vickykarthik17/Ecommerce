# E-Commerce ETL Pipeline

An end-to-end batch ETL pipeline built with Python and PostgreSQL, using the Olist Brazilian E-Commerce Public Dataset as the source data.

The pipeline extracts raw e-commerce data, validates the source files, transforms the datasets based on business meaning and profiling findings, loads the processed data into PostgreSQL, and performs database-level validation with full logging and error handling along the way.

---

## 1. Project Overview

The pipeline follows a straightforward, linear flow:

```
Olist CSV Files
        |
Extraction
        |
Source Validation
        |
Transformation
        |
Transformation Validation
        |
PostgreSQL Loading
        |
Database Validation
        |
Logging & Error Handling
```

The project demonstrates a repeatable batch ETL workflow using a full-refresh loading strategy, which fits well given that the source dataset is static and historical rather than continuously updated.

---

## 2. Dataset

**Dataset used:** Olist Brazilian E-Commerce Public Dataset

The dataset contains roughly 100,000 orders from a Brazilian e-commerce marketplace, spread across the following files:

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

Together, these datasets present a good range of real-world data challenges: one-to-many relationships, missing values, duplicate observations, tricky identifier logic, datatype mismatches, and referential integrity constraints.

---

## 3. Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas |
| Database | PostgreSQL 18 |
| Database Driver | psycopg |
| Configuration | python-dotenv |
| Version Control | Git & GitHub |
| Data Format | CSV |

---

## 4. ETL Components

### Extraction

- Reads all nine source CSV files.
- Checks that every expected source file is actually present.
- Validates expected columns before any transformation begins.
- Reports source row and column counts for visibility.

### Transformation

Transformations are driven by data profiling and business context, not by blanket rules that strip out anything unusual. The pipeline:

- Standardizes data types.
- Normalizes selected text fields.
- Converts date columns into proper date formats.
- Preserves NULL values where they carry legitimate meaning.
- Removes confirmed exact duplicate records where that's justified.
- Keeps legitimate repeated identifiers intact in one-to-many relationships.
- Renames inconsistent source columns for clarity.
- Prepares PostgreSQL-compatible processed CSV files ready for loading.

### Loading

Processed datasets are loaded into PostgreSQL using the `COPY` command for efficient bulk ingestion.

The loading process follows a full-refresh approach:

```
TRUNCATE existing tables
        |
Bulk load processed CSV files
        |
Validate database
```

This approach makes sense here because the Olist source is a static historical snapshot, not a live production feed that changes continuously.

### Validation

Validation happens at multiple stages throughout the pipeline:

1. Source file and column validation
2. Transformation-level row, column, and NULL validation
3. Duplicate-key validation
4. Database row-count validation
5. Primary and composite-key validation
6. Foreign-key validation
7. Referential-integrity validation

---

## 5. Logging and Error Handling

The pipeline keeps a detailed record of its execution, including:

- Pipeline start and completion times
- Each individual ETL step
- Step-level execution time
- Error output and full tracebacks
- Any failed pipeline steps

Logs are written to:

```
logs/pipeline.log
```

If a dependent step fails, the orchestrator stops the pipeline immediately rather than continuing forward with potentially invalid data.

---

## 6. Project Structure

```
Ecommerce/
|
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- profiling/
|
|-- docs/
|   |-- 02_business_context.md
|   |-- 03_data_profiling.md
|   |-- 04_transformation_process.md
|   |-- 05_validation_strategy.md
|   |-- 06_data_dictionary.md
|   |-- 07_loading_and_database.md
|   |-- 08_logging_and_error_handling.md
|   `-- 09_challenges_and_solutions.md
|
|-- sql/
|   `-- schema.sql
|
|-- src/
|   |-- extraction/
|   |   |-- expected_columns.py
|   |   |-- extract_data.py
|   |   `-- validate_data.py
|   |
|   |-- profiling/
|   |   |-- analyse_keys.py
|   |   |-- analyse_relationships.py
|   |   |-- investigate_geolocation.py
|   |   |-- investigate_reviews.py
|   |   `-- profile_sources.py
|   |
|   |-- transformation/
|   |   |-- transform_category_translation.py
|   |   |-- transform_customers.py
|   |   |-- transform_geolocation.py
|   |   |-- transform_orders.py
|   |   |-- transform_order_items.py
|   |   |-- transform_payments.py
|   |   |-- transform_products.py
|   |   |-- transform_reviews.py
|   |   |-- transform_sellers.py
|   |   `-- validate_all.py
|   |
|   |-- loading/
|   |   |-- db_config.py
|   |   |-- load_data.py
|   |   |-- load_geolocation.py
|   |   |-- test_connection.py
|   |   `-- validate_database.py
|   |
|   |-- logging_config.py
|   `-- run_pipeline.py
|
|-- .gitignore
|-- README.md
`-- requirements.txt
```

---

## 7. Documentation Guide (Recommended Reading Order)

For anyone reviewing this project for the first time, it's easiest to follow this order:

```
README.md
        |
02_business_context.md
        |
03_data_profiling.md
        |
06_data_dictionary.md
        |
04_transformation_process.md
        |
05_validation_strategy.md
        |
07_loading_and_database.md
        |
08_logging_and_error_handling.md
        |
09_challenges_and_solutions.md
```

This sequence mirrors the actual thought process behind the project:

```
What is the project?
        |
What does the business data mean?
        |
What did we discover in the raw data?
        |
What does each field mean?
        |
What did we transform and why?
        |
How did we validate it?
        |
How was it loaded into PostgreSQL?
        |
How does the pipeline handle execution and failures?
        |
What problems did we encounter and solve?
```

---

## 8. Setup and Usage

### Step 1: Clone the Repository

```bash
git clone https://github.com/vickykarthik17/Ecommerce.git
cd Ecommerce
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure PostgreSQL

Create a `.env` file in the project root with the following values:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
```

### Step 4: Create the Database

Create a PostgreSQL database named `ecommerce`, then apply the schema:

```bash
psql -U postgres -d ecommerce -f sql/schema.sql
```

### Step 5: Run the Complete Pipeline

From the project root, run:

```bash
python src/run_pipeline.py
```

The orchestrator runs extraction, validation, transformation, PostgreSQL loading, and final database validation, all in sequence.

If any step fails, the pipeline catches the subprocess error, logs which step failed, and stops execution rather than pushing forward.

---

## 9. Data Quality Philosophy

The pipeline doesn't automatically strip out every NULL or repeated value it finds. Instead, data-quality decisions are grounded in what each dataset actually means and what the target PostgreSQL schema requires.

A few examples of that reasoning in practice:

- Missing delivery dates can be entirely valid, depending on where an order sits in its lifecycle.
- Review comments are optional fields, so a blank one isn't a data quality issue.
- Repeated geolocation ZIP prefixes can legitimately represent different coordinates.
- Review uniqueness is validated using `review_id + order_id`.
- Order-item uniqueness is validated using `order_id + order_item_id`.
- Payment uniqueness is validated using `order_id + payment_sequential`.

This approach avoids the common trap of deleting valid business records just because a value happens to repeat or appear missing.

---

## 10. Key Challenges

**1. Geolocation Duplicates**

The raw geolocation dataset contained both exact duplicate rows and multiple genuinely valid records sharing the same ZIP prefix.

*Solution:* Remove only the exact duplicates while preserving valid repeated ZIP prefixes. The processed dataset ended up with 738,327 rows, down from 1,000,163 raw rows.

**2. Review Identifiers**

Individual `review_id` values weren't sufficient on their own to guarantee uniqueness.

*Solution:* Use `review_id + order_id` together as the composite database key.

**3. PostgreSQL Integer Loading**

Some product integer attributes were being written to CSV as float-like values, such as `40.0`.

*Solution:* Align the transformed values with the PostgreSQL integer schema before running the bulk load.

**4. Repeat-Safe Loading**

Rerunning the pipeline against existing tables caused duplicate-key conflicts.

*Solution:* Adopt a full-refresh strategy using `TRUNCATE ... CASCADE` before each bulk load.

**5. Pipeline Failure Handling**

A controlled failure was deliberately introduced to confirm the orchestrator would catch errors and halt downstream processing correctly.

*Result:* The failed step and its traceback were logged as expected, and the pipeline stopped exactly as designed.

---

## 11. Validation Results

The most recent successful end-to-end run loaded the following row counts:

| # | Dataset | Rows |
|---|---|---:|
| 1 | Customers | 99,441 |
| 2 | Orders | 99,441 |
| 3 | Order Items | 112,650 |
| 4 | Payments | 103,886 |
| 5 | Reviews | 99,224 |
| 6 | Products | 32,951 |
| 7 | Sellers | 3,095 |
| 8 | Geolocation | 738,327 |
| 9 | Category Translation | 71 |

Database key validation and foreign-key validation both completed successfully.

The full pipeline execution finished end to end in approximately 69.48 seconds.

---

## 12. Project Scope

### In Scope

- End-to-end ETL
- Data extraction
- Source validation
- Data profiling
- Business-driven data transformation
- Data-quality validation
- PostgreSQL schema design
- PostgreSQL bulk loading using `COPY`
- Database validation
- Pipeline orchestration
- Execution logging
- Error handling
- Repeatable full-refresh execution
- Project documentation

### Out of Scope

- Continuous data ingestion
- Production scheduling
- Incremental or CDC (change data capture) loading
- Cloud deployment
- Streaming ingestion

These were deliberately left out of scope. Since the source is a static historical dataset, the project's real objective was to demonstrate a complete, well-validated batch ETL workflow rather than a production-grade streaming system.

---

## 13. Key Learning

This project shows how raw relational datasets can be turned into validated, well-structured data and loaded into PostgreSQL through a repeatable ETL pipeline.

Beyond that, it reflects a number of practical engineering decisions, including:

- Profiling data before cleaning it
- Defining transformation rules based on business meaning
- Designing primary and composite keys
- Enforcing referential integrity
- Interpreting NULLs correctly rather than removing them by default
- Investigating duplicates before deleting them
- Handling PostgreSQL datatype compatibility issues
- Bulk loading efficiently
- Running full-refresh batch processing
- Orchestrating the pipeline end to end
- Logging and error handling
- Investigating and recovering from failures

The guiding principle throughout the project can be summed up as:

```
Understand the data
        |
Profile the data
        |
Define business meaning
        |
Transform deliberately
        |
Validate
        |
Load into PostgreSQL
        |
Validate again
        |
Log and monitor execution
```
