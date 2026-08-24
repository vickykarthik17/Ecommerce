# E-Commerce ETL Pipeline

An end-to-end batch ETL pipeline built with Python and PostgreSQL using the Olist Brazilian E-Commerce Public Dataset.

The pipeline extracts raw e-commerce data, validates source files, transforms the datasets based on business meaning and profiling findings, loads the processed data into PostgreSQL, and performs database-level validation with logging and error handling.

1. Project Overview

Olist CSV Files
      â†“
Extraction
      â†“
Source Validation
      â†“
Transformation
      â†“
Transformation Validation
      â†“
PostgreSQL Loading
      â†“
Database Validation
      â†“
Logging & Error Handling

The project demonstrates a repeatable batch ETL workflow with a full-refresh loading strategy appropriate for the static historical source dataset.

2. Dataset

Dataset: Olist Brazilian E-Commerce Public Dataset

The dataset contains approximately 100,000 orders from a Brazilian e-commerce marketplace and includes:

Customers

Orders

Order Items

Payments

Reviews

Products

Sellers

Geolocation

Product Category Translation

The related datasets provide practical scenarios involving one-to-many relationships, missing values, duplicate observations, identifier analysis, datatype mismatches, and relational integrity.

3. Technology Stack

Area

Technology

Programming

Python

Data Processing

Pandas

Database

PostgreSQL 18

Database Driver

psycopg

Configuration

python-dotenv

Version Control

Git & GitHub

Data Format

CSV

4. ETL Components

Extraction

Reads all nine source CSV files.

Checks that expected source files are present.

Validates expected columns before transformation.

Reports source row and column counts.

Transformation

Transformations are based on profiling and business meaning rather than blindly removing values.

The pipeline:

Standardizes data types.

Normalizes selected text fields.

Converts date columns.

Preserves meaningful NULL values.

Removes confirmed exact duplicate observations where justified.

Preserves legitimate repeated identifiers in one-to-many relationships.

Renames inconsistent source columns.

Prepares PostgreSQL-compatible processed CSV files.

Loading

Processed datasets are loaded into PostgreSQL using PostgreSQL COPY for efficient bulk ingestion.

The loading process uses a full-refresh approach:

TRUNCATE existing tables
        â†“
Bulk load processed CSV files
        â†“
Validate database

This is appropriate because the Olist source is a static historical snapshot rather than a continuously changing production feed.

Validation

Validation is performed at multiple stages:

Source file and column validation

Transformation row/column/NULL validation

Duplicate-key validation

Database row-count validation

Primary and composite-key validation

Foreign-key validation

Referential-integrity validation

Logging and Error Handling

The pipeline records:

Pipeline start and completion

Individual ETL steps

Step execution time

Error output and tracebacks

Failed pipeline steps

Logs are written to:

logs/pipeline.log

The orchestrator stops the pipeline when a dependent step fails instead of continuing with potentially invalid data.

5. Project Structure

Ecommerce/
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ raw/
â”‚   â”œâ”€â”€ processed/
â”‚   â””â”€â”€ profiling/
â”‚
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ 02_business_context.md
â”‚   â”œâ”€â”€ 03_data_profiling.md
â”‚   â”œâ”€â”€ 04_transformation_process.md
â”‚   â”œâ”€â”€ 05_validation_strategy.md
â”‚   â”œâ”€â”€ 06_data_dictionary.md
â”‚   â”œâ”€â”€ 07_loading_and_database.md
â”‚   â”œâ”€â”€ 08_logging_and_error_handling.md
â”‚   â””â”€â”€ 09_challenges_and_solutions.md
â”‚
â”œâ”€â”€ sql/
â”‚   â””â”€â”€ schema.sql
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ extraction/
â”‚   â”‚   â”œâ”€â”€ expected_columns.py
â”‚   â”‚   â”œâ”€â”€ extract_data.py
â”‚   â”‚   â””â”€â”€ validate_data.py
â”‚   â”‚
â”‚   â”œâ”€â”€ profiling/
â”‚   â”‚   â”œâ”€â”€ analyse_keys.py
â”‚   â”‚   â”œâ”€â”€ analyse_relationships.py
â”‚   â”‚   â”œâ”€â”€ investigate_geolocation.py
â”‚   â”‚   â”œâ”€â”€ investigate_reviews.py
â”‚   â”‚   â””â”€â”€ profile_sources.py
â”‚   â”‚
â”‚   â”œâ”€â”€ transformation/
â”‚   â”‚   â”œâ”€â”€ transform_category_translation.py
â”‚   â”‚   â”œâ”€â”€ transform_customers.py
â”‚   â”‚   â”œâ”€â”€ transform_geolocation.py
â”‚   â”‚   â”œâ”€â”€ transform_orders.py
â”‚   â”‚   â”œâ”€â”€ transform_order_items.py
â”‚   â”‚   â”œâ”€â”€ transform_payments.py
â”‚   â”‚   â”œâ”€â”€ transform_products.py
â”‚   â”‚   â”œâ”€â”€ transform_reviews.py
â”‚   â”‚   â”œâ”€â”€ transform_sellers.py
â”‚   â”‚   â””â”€â”€ validate_all.py
â”‚   â”‚
â”‚   â”œâ”€â”€ loading/
â”‚   â”‚   â”œâ”€â”€ db_config.py
â”‚   â”‚   â”œâ”€â”€ load_data.py
â”‚   â”‚   â”œâ”€â”€ load_geolocation.py
â”‚   â”‚   â”œâ”€â”€ test_connection.py
â”‚   â”‚   â””â”€â”€ validate_database.py
â”‚   â”‚
â”‚   â”œâ”€â”€ logging_config.py
â”‚   â””â”€â”€ run_pipeline.py
â”‚
â”œâ”€â”€ tests/
â”œâ”€â”€ .gitignore
â”œâ”€â”€ README.md
â””â”€â”€ requirements.txt

6. Documentation / Recommended Study Order

For someone reviewing the project for the first time, the recommended order is:

README.md
    â†“
02_business_context.md
    â†“
03_data_profiling.md
    â†“
06_data_dictionary.md
    â†“
04_transformation_process.md
    â†“
05_validation_strategy.md
    â†“
07_loading_and_database.md
    â†“
08_logging_and_error_handling.md
    â†“
09_challenges_and_solutions.md

This follows the reasoning behind the project:

What is the project?
        â†“
What does the business data mean?
        â†“
What did we discover in the raw data?
        â†“
What does each field mean?
        â†“
What did we transform and why?
        â†“
How did we validate it?
        â†“
How was it loaded into PostgreSQL?
        â†“
How does the pipeline handle execution and failures?
        â†“
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

Missing delivery dates can be valid depending on order lifecycle state.

Review comments are optional fields.

Repeated geolocation ZIP prefixes can represent different coordinates.

Review uniqueness is validated using review_id + order_id.

Order-item uniqueness is validated using order_id + order_item_id.

Payment uniqueness is validated using order_id + payment_sequential.

This approach prevents valid business records from being removed simply because a value is repeated or missing.

9. Key Challenges

Geolocation Duplicates

The raw geolocation dataset contained exact duplicate observations as well as multiple valid records for the same ZIP prefix.

Solution: Remove only exact duplicate rows and preserve valid repeated ZIP prefixes. The processed dataset contains 738,327 rows from 1,000,163 raw rows.

Review Identifiers

Individual review_id values were not sufficient to establish uniqueness.

Solution: Use review_id + order_id as the composite database key.

PostgreSQL Integer Loading

Some product integer attributes were written to CSV as values such as 40.0.

Solution: Align the transformed values with the PostgreSQL integer schema before bulk loading.

Repeat-Safe Loading

Rerunning the same complete dataset against existing tables caused duplicate-key conflicts.

Solution: Use a full-refresh strategy with TRUNCATE ... CASCADE before bulk loading.

Pipeline Failure Handling

A controlled failure was used to verify that the orchestrator captures errors and stops downstream processing.

Result: The failed step and traceback were logged and the pipeline stopped as designed.

10. Validation Result

The latest successful end-to-end run loaded:

Dataset

Rows

Customers

99,441

Orders

99,441

Order Items

112,650

Payments

103,886

Reviews

99,224

Products

32,951

Sellers

3,095

Geolocation

738,327

Category Translation

71

Database key validation and foreign-key validation completed successfully.

The latest full pipeline execution completed successfully in approximately 69.48 seconds.

11. Project Scope

Included

End-to-end ETL

Data extraction

Source validation

Data profiling

Business-driven data transformation

Data-quality validation

PostgreSQL schema design

PostgreSQL bulk loading using COPY

Database validation

Pipeline orchestration

Execution logging

Error handling

Repeatable full-refresh execution

Project documentation

Continuous data ingestion

Production scheduling

Incremental or CDC loading

Cloud deployment

Streaming ingestion

These were intentionally kept outside the current scope because the source is a static historical dataset and the project objective is to demonstrate a complete batch ETL workflow.

12. Key Learning

This project demonstrates how raw relational datasets can be transformed into validated, structured data and loaded into PostgreSQL through a repeatable ETL pipeline.

The project also demonstrates practical engineering decisions around:

Data profiling before cleaning

Business-driven transformation rules

Primary and composite key design

Referential integrity

NULL interpretation

Duplicate investigation

PostgreSQL datatype compatibility

Bulk loading

Full-refresh batch processing

Pipeline orchestration

Logging and error handling

Failure investigation and recovery

The central principle is:

Understand the data
        â†“
Profile the data
        â†“
Define business meaning
        â†“
Transform deliberately
        â†“
Validate
        â†“
Load into PostgreSQL
        â†“
Validate again
        â†“
Log and monitor execution