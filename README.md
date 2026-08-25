# E-Commerce ETL Pipeline

An end-to-end batch ETL pipeline built with Python and PostgreSQL using the Olist Brazilian E-Commerce Public Dataset.

The pipeline extracts raw e-commerce data, validates source files, transforms the datasets based on business meaning and profiling findings, loads the processed data into PostgreSQL, and performs database-level validation with logging and error handling.

1. Project Overview

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

The project demonstrates a repeatable batch ETL workflow with a full-refresh loading strategy appropriate for the static historical source dataset.

2. Dataset

Dataset: Olist Brazilian E-Commerce Public Dataset

The dataset contains approximately 100,000 orders from a Brazilian e-commerce marketplace and includes:

1. Customers

2. Orders

3. Order Items

4. Payments

5. Reviews

6. Products

7. Sellers

8. Geolocation

9. Product Category Translation

The related datasets provide practical scenarios involving one-to-many relationships, missing values, duplicate observations, identifier analysis, datatype mismatches, and relational integrity.

3. Technology Stack

1. Area/Technology

2. Programming - Python

3. Data Processing - Pandas

4. Database - PostgreSQL 18

5. Database Driver - psycopg

6. Configuration - python-dotenv

7. Version Control - Git & GitHub

8. Data Format - CSV

4. ETL Components

Extraction:

1. Reads all nine source CSV files.

2. Checks that expected source files are present.

3. Validates expected columns before transformation.

4. Reports source row and column counts.

Transformation: 

Transformations are based on profiling and business meaning rather than blindly removing values.

The pipeline:

1. Standardizes data types.

2. Normalizes selected text fields.

3. Converts date columns.

4. Preserves meaningful NULL values.

5. Removes confirmed exact duplicate observations where justified.

6. Preserves legitimate repeated identifiers in one-to-many relationships.

7. Renames inconsistent source columns.

8. Prepares PostgreSQL-compatible processed CSV files.

Loading:

Processed datasets are loaded into PostgreSQL using PostgreSQL COPY for efficient bulk ingestion.

The loading process uses a full-refresh approach:

TRUNCATE existing tables
        |
Bulk load processed CSV files
        |
Validate database


This is appropriate because the Olist source is a static historical snapshot rather than a continuously changing production feed.

Validation:

Validation is performed at multiple stages:

1. Source file and column validation

2. Transformation row/column/NULL validation

3. Duplicate-key validation

4. Database row-count validation

5. Primary and composite-key validation

6. Foreign-key validation

7. Referential-integrity validation

Logging and Error Handling

The pipeline records:

1. Pipeline start and completion

2. Individual ETL steps

3. Step execution time

4. Error output and tracebacks

5. Failed pipeline steps

Logs are written to:

logs/pipeline.log

The orchestrator stops the pipeline when a dependent step fails instead of continuing with potentially invalid data.

5. Project Structure

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
|-- tests/
|-- .gitignore
|-- README.md
`-- requirements.txt

6. Documentation / Recommended Study Order

For someone reviewing the project for the first time, the recommended order is:

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

This follows the reasoning behind the project:

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

7. Running the Pipeline

Step 1: Clone the Repository

git clone https://github.com/vickykarthik17/Ecommerce.git
cd Ecommerce

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Configure PostgreSQL

Create a .env file in the project root:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

Step 4: Create the Database

Create a PostgreSQL database named:

ecommerce

Then apply the schema:

psql -U postgres -d ecommerce -f sql/schema.sql

Step 5: Run the Complete Pipeline

From the project root:

python src/run_pipeline.py

The orchestrator runs extraction, validation, transformation, PostgreSQL loading, and final database validation in sequence.

If a step fails, the pipeline captures the subprocess error, logs the failed step, and stops execution.

8. Data Quality Philosophy

The pipeline does not automatically remove every NULL or repeated value.

Data-quality decisions are based on the meaning of each dataset and the requirements of the target PostgreSQL schema.

Examples:

1. Missing delivery dates can be valid depending on order lifecycle state.

2. Review comments are optional fields.

3. Repeated geolocation ZIP prefixes can represent different coordinates.

4. Review uniqueness is validated using review_id + order_id.

5. Order-item uniqueness is validated using order_id + order_item_id.

6. Payment uniqueness is validated using order_id + payment_sequential.

This approach prevents valid business records from being removed simply because a value is repeated or missing.

9. Key Challenges

1. Geolocation Duplicates

The raw geolocation dataset contained exact duplicate observations as well as multiple valid records for the same ZIP prefix.

Solution: Remove only exact duplicate rows and preserve valid repeated ZIP prefixes. The processed dataset contains 738,327 rows from 1,000,163 raw rows.

2. Review Identifiers

Individual review_id values were not sufficient to establish uniqueness.

Solution: Use review_id + order_id as the composite database key.

3. PostgreSQL Integer Loading

Some product integer attributes were written to CSV as values such as 40.0.

Solution: Align the transformed values with the PostgreSQL integer schema before bulk loading.

4. Repeat-Safe Loading

Rerunning the same complete dataset against existing tables caused duplicate-key conflicts.

Solution: Use a full-refresh strategy with TRUNCATE ... CASCADE before bulk loading.

5. Pipeline Failure Handling

A controlled failure was used to verify that the orchestrator captures errors and stops downstream processing.

Result: The failed step and traceback were logged and the pipeline stopped as designed.

10. Validation Result

The latest successful end-to-end run loaded:

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

Database key validation and foreign-key validation completed successfully.

The latest full pipeline execution completed successfully in approximately 69.48 seconds.

11. Project Scope

Included

1. End-to-end ETL

2. Data extraction

3. Source validation

4. Data profiling

5. Business-driven data transformation

6. Data-quality validation

7. PostgreSQL schema design

8. PostgreSQL bulk loading using COPY

9. Database validation

10. Pipeline orchestration

11. Execution logging

12. Error handling

13. Repeatable full-refresh execution

14. Project documentation

1. Continuous data ingestion

2. Production scheduling

3. Incremental or CDC loading

4. Cloud deployment

5. Streaming ingestion

These were intentionally kept outside the current scope because the source is a static historical dataset and the project objective is to demonstrate a complete batch ETL workflow.

12. Key Learning

This project demonstrates how raw relational datasets can be transformed into validated, structured data and loaded into PostgreSQL through a repeatable ETL pipeline.

The project also demonstrates practical engineering decisions around:

1. Data profiling before cleaning

2. Business-driven transformation rules

3. Primary and composite key design

4. Referential integrity

5. NULL interpretation

6. Duplicate investigation

7. PostgreSQL datatype compatibility

8. Bulk loading

9. Full-refresh batch processing

10. Pipeline orchestration

11. Logging and error handling

12. Failure investigation and recovery

The central principle is:

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