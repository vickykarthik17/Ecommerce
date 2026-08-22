# E-Commerce Orders & Customer Analytics ETL

An end-to-end batch ETL pipeline built with Python and PostgreSQL using the Olist Brazilian E-Commerce Public Dataset.

The pipeline extracts raw e-commerce data, validates the source files, transforms and cleans the datasets, loads the processed data into PostgreSQL, and performs database-level validation.

---

## 1. Project Overview

The project demonstrates a complete ETL workflow:

```text
Olist CSV Files
      :
      ↓
Extraction
      :
      ↓
Source Validation
      :
      ↓
Transformation
      :
      ↓
Data Quality Validation
      :
      ↓
PostgreSQL Loading
      :
      ↓
Database Validation
      :
      ↓
Logging & Error Handling

The pipeline is designed as a reusable batch process and supports repeatable full-refresh execution.

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

The datasets contain multiple relationships and different data-quality scenarios, making them suitable for demonstrating an end-to-end ETL process.

3. Technology Stack
Area	Technology
Programming	Python
Data Processing	Pandas
Database	PostgreSQL 18
Database Driver	psycopg
Configuration	python-dotenv
Version Control	Git & GitHub
Data Format	CSV
4. ETL Components
Extraction
Reads all nine source CSV files.
Validates expected columns.
Checks source files before transformation.
Transformation
Standardizes data types.
Normalizes text fields.
Converts date columns.
Handles meaningful missing values.
Removes confirmed exact duplicates.
Renames inconsistent source columns.
Prepares CSV files for PostgreSQL.
Loading

Processed datasets are loaded into PostgreSQL using PostgreSQL COPY for efficient bulk loading.

The loading process uses a full-refresh approach:

TRUNCATE existing tables
        :
        ↓
Bulk load processed CSV files
Validation

Validation is performed at multiple stages:

Source validation
Transformation validation
Database row-count validation
Primary/composite key validation
Foreign-key relationship validation
Logging

The pipeline records:

Pipeline start and completion
Individual ETL steps
Step execution time
Errors and tracebacks
Failed pipeline steps

Logs are stored in:

logs/pipeline.log
5. Project Structure
Ecommerce/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── 06_data_dictionary.md
│   └── 07_transformation_rules.md
│
├── sql/
│   └── schema.sql
│
├── src/
│   ├── extraction/
│   ├── profiling/
│   ├── transformation/
│   ├── loading/
│   ├── logging_config.py
│   └── run_pipeline.py
│
├── .gitignore
├── README.md
└── requirements.txt
6. Running the Pipeline
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

If a step fails, the pipeline records the error and stops execution.

7. Data Quality Handling

The pipeline does not automatically remove every null or repeated value.

Data quality decisions are based on the meaning of each dataset.

Examples:

Missing delivery dates can be valid for certain order statuses.
Review comments are optional fields.
Repeated geolocation ZIP prefixes can represent different coordinates.
Review uniqueness is validated using review_id + order_id.
Order-item uniqueness is validated using order_id + order_item_id.

This prevents valid business data from being removed during transformation.

8. Key Challenges
Geolocation Duplicates

The geolocation dataset contained exact duplicate rows as well as multiple valid records for the same ZIP prefix.

Solution: Remove only exact duplicate rows and preserve valid repeated ZIP prefixes.

Review Identifiers

Individual review_id values were repeated in the source data.

Solution: Use review_id + order_id as the composite business key.

PostgreSQL Integer Loading

Some product integer attributes were written to CSV as values such as 40.0.

Solution: Convert these values to integer-formatted strings before PostgreSQL bulk loading.

Pipeline Failure Handling

A controlled failure test was used to verify pipeline behavior.

Result: The orchestrator captured the error, identified the failed step, and stopped subsequent processing.

9. Validation Result

The final pipeline successfully loaded:

Dataset	Rows
Customers	99,441
Orders	99,441
Order Items	112,650
Payments	103,886
Reviews	99,224
Products	32,951
Sellers	3,095
Geolocation	738,327
Category Translation	71

Database key and foreign-key validation completed successfully.

10. Project Scope
Included
End-to-end ETL
Data extraction
Source validation
Data transformation
Data quality validation
PostgreSQL schema design
Bulk loading
Database validation
Pipeline orchestration
Logging
Error handling
Repeatable full-refresh execution
Not Included
Power BI dashboards
Continuous data ingestion
Production scheduling
Incremental/CDC loading
Cloud deployment
11. Key Learning

This project demonstrates how raw relational datasets can be transformed into validated, structured data and loaded into a PostgreSQL database through a repeatable ETL pipeline.

It also demonstrates practical handling of data-quality issues, database constraints, bulk loading, pipeline failures, and execution logging.

