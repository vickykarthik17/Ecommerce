i have downloaded the dataset from kaggle.. what should i do now?

 this is the current folder structure now..remember that my mai folder name is Ecommerce .. not ecommerce-etl-pipeline

i want you to make this type of data meaningful.. include meaningful separatorsv like :  and keep the sentences and points meaninful 

Tuesday 2:14 PM
it is showing like this..what should my path be?

 no output

Pasted markdown.md
File
this is the exact project doc 06_data_dictionary.md

what to select?





it is not showing output

loaded 


Pasted markdown(1).md
File
this document doesn,t seem meaningful.. can you make it ordered, structured , date by date, and also include blockers you faced in every sprint, and how you;ve tackled them,, make it a good Document, i could present and preserve

Yes. I’ve expanded it substantially rather than just adding a few paragraphs.

The new version is 2,455 lines and includes:

    Detailed project overview and objectives

    Why Olist was selected

    Complete technology stack

    ETL architecture

    Detailed date-by-date development history

    Sprint-wise objectives, work, findings, blockers, resolutions, and outcomes

    Detailed transformation rules for all 9 datasets

    PostgreSQL schema and relationship explanation

    Primary/composite key decisions

    Detailed loading process

    The actual PostgreSQL timestamp/NaN blocker and resolution

    Duplicate product loading issue

    Geolocation bulk-loading decision

    Data-quality findings and reasoning

    Full source data dictionary

    Project structure

    Git/repository practices

    Lessons learned

    Automation design

    Failure scenarios

    Current status and remaining work

    Completion criteria

    Final project summary

    Quick-reference section

I also kept a clear distinction between completed work, pending validation, and future planned work, so the document doesn't falsely claim that future tasks are already completed.

Download the elaborated document:


IT IS A SOLO PROJECT, SO IT wouldnt involve any discussions with any team,, so make it accordingly

Absolutely. Since this is a solo project, the documentation should describe the work as your own investigation, implementation, decisions, and troubleshooting, not as team collaboration.

I would change the wording throughout the document like this:
Remove team-oriented language

Avoid phrases such as:

    “team discussions”

    “discussed with the team”

    “team decided”

    “team review”

    “assigned tasks”

    “team members”

    “collaborated with”

    “peer review”

    “sprint meeting”

    “team feedback”

Use solo-project wording

Instead:

    “I investigated…”

    “I identified…”

    “I evaluated…”

    “I decided to…”

    “I implemented…”

    “During development, I encountered…”

    “I resolved this by…”

    “I validated…”

    “I documented…”

    “The next step was…”

For example:

    Before:
    The team investigated the duplicate review IDs and decided to use a composite key.

    Better:
    During data profiling, I identified repeated review_id values. I investigated whether these represented duplicate records and found that (review_id, order_id) was unique. Based on this validation, I used the composite key rather than removing records unnecessarily.

And for Scrum:

    Before:
    Sprint planning and team discussions were used to determine the next tasks.

    Better:
    I organized the project into short development sprints to structure the work, track progress, and validate each ETL stage before moving to the next stage.

Important distinction

You can still use Agile/Scrum methodology for a solo project. The sprint concept is useful for organizing your own development work. Just don't imply that Scrum ceremonies involved multiple people.

So your project documentation should essentially tell this story:

I planned the project
       ↓
I investigated the source data
       ↓
I identified data-quality issues
       ↓
I designed the transformations
       ↓
I implemented the ETL stages
       ↓
I encountered technical blockers
       ↓
I investigated and resolved them
       ↓
I validated the results
       ↓
I documented the implementation

That will actually make the project stronger for interviews, because you can clearly explain what you personally did and why you made each engineering decision.

If you want, I can also rewrite the entire 2,455-line document specifically as a solo-project development journal, while keeping the technical detail and making the language presentation-ready.

rewrite

Done. I rewrote the document specifically as a solo project, while keeping it detailed and presentation-ready.

The revised version now consistently uses “I implemented,” “I investigated,” “I identified,” “I resolved,” “I validated” instead of implying team discussions or collaboration.

It also explicitly explains that Scrum is being used as a personal sprint-based development framework, not as a team process.
Download

The new version is 2,799 lines and includes the detailed development history, blockers and resolutions, technical decisions, PostgreSQL work, transformation details, validation, and future automation without inventing team involvement.


Library
/06_data_dictionary_solo_project.md
E-Commerce End-to-End ETL Pipeline
Project Documentation, Data Dictionary and Development History

Project: E-Commerce Orders & Customer Analytics ETL
Project Type: Solo End-to-End ETL Project
Dataset: Olist Brazilian E-Commerce Public Dataset
Methodology: Agile Scrum-inspired sprint planning
Primary Language: Python
Database: PostgreSQL
Analytics: SQL and Power BI
Project Start Date: 10 August 2026
Target Completion Date: 25 August 2026
Current Stage: Sprint 3, PostgreSQL and Data Loading
Repository: https://github.com/vickykarthik17/Ecommerce.git
1. Project Overview
1.1 Project Description

This project is a solo implementation of an end-to-end ETL pipeline using the Olist Brazilian E-Commerce Public Dataset.

The objective is to take raw e-commerce CSV files through a structured data engineering workflow:

Raw Data
   |
   v
Source Profiling
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
PostgreSQL Loading
   |
   v
Database Validation
   |
   v
SQL / Power BI Analytics

I am developing the project independently, which means all source investigation, technical decisions, implementation, troubleshooting, validation, documentation, and project planning are performed by me.

There are no team members involved in the implementation. The sprint structure is being used only as a way to organize and track my own development work.

The project is intentionally being built in stages instead of creating one large script. This allows me to validate each ETL layer independently before connecting it to the next stage.
2. Project Objectives

The main objectives of the project are:

    Understand the structure of the Olist e-commerce dataset.

    Profile all source datasets before modifying any data.

    Identify missing values, duplicates, candidate keys, and relationships.

    Investigate unusual data-quality patterns instead of assuming they are errors.

    Build a reusable extraction layer using Python.

    Validate source files before allowing them into later ETL stages.

    Apply documented transformation rules.

    Preserve meaningful business information while cleaning the data.

    Generate processed datasets suitable for database loading.

    Design a relational PostgreSQL database.

    Define appropriate primary keys and composite keys.

    Define foreign-key relationships.

    Load the processed datasets into PostgreSQL.

    Validate database row counts and relationships.

    Record technical blockers encountered during development.

    Document how each blocker was investigated and resolved.

    Prepare the pipeline for later automation and end-to-end testing.

    Build a foundation for SQL analysis and Power BI reporting.

3. Why I Chose the Olist Dataset

I selected the Olist dataset because it represents a realistic e-commerce marketplace environment and contains multiple related business entities.

The dataset is not a single flat CSV. It contains information about:

    Customers

    Orders

    Order items

    Payments

    Reviews

    Products

    Sellers

    Geolocation

    Product category translations

This makes it suitable for demonstrating a complete ETL process.

The dataset provides several practical data-engineering challenges, including:

    Multiple source files

    Different table sizes

    One-to-many relationships

    Candidate primary keys

    Composite keys

    Missing values

    Duplicate records

    Date and timestamp fields

    Text normalization

    Geographic data

    Referential integrity

    Database constraints

    Large-volume data loading

Because the project is intended to demonstrate practical ETL skills, I wanted a dataset where I would have to make actual data-engineering decisions rather than simply clean one CSV file.
4. Why This Is a Solo Project

This project is being developed independently from start to finish.

I am responsible for:

    Project planning

    Dataset selection

    Source investigation

    Data profiling

    ETL architecture

    Python implementation

    Transformation design

    PostgreSQL schema design

    Data loading

    Validation

    Troubleshooting

    Git version control

    Documentation

    Future automation

    Final presentation

The sprint methodology is therefore being used as a personal development framework.

For example:

Sprint
   |
   +-- Define my objective
   +-- Implement the required work
   +-- Validate the result
   +-- Record problems encountered
   +-- Resolve the problems
   +-- Document the outcome
   +-- Move to the next stage

There are no team assignments or team discussions involved in the project.
5. Technology Stack
Area	Technology
Programming	Python
Data Processing	Pandas
Database	PostgreSQL 18
Database Driver	psycopg
Database Administration	pgAdmin 4
Configuration	python-dotenv
Version Control	Git
Repository	GitHub
Analytics	SQL, Power BI
Methodology	Agile Scrum-inspired sprint planning
6. Project Methodology

Although this is a solo project, I am following a sprint-based Agile approach to structure the development.

The work is divided into manageable stages so that I can complete and validate one part of the ETL pipeline before moving to another.
Sprint Plan
Sprint	Dates	Focus	Expected Output
Sprint 1	Aug 10 - Aug 13	Requirements, profiling, extraction	Validated source layer
Sprint 2	Aug 14 - Aug 17	Transformation and data quality	Processed datasets
Sprint 3	Aug 18 - Aug 21	PostgreSQL and loading	Populated database
Sprint 4	Aug 22 - Aug 24	Automation and testing	Integrated pipeline
Final Release	Aug 25	Documentation and final review	Completed project

The documentation distinguishes between planned work and work that I have actually completed.

Future tasks are not marked as completed until I have implemented and validated them.
7. Dataset Overview

The project uses nine Olist source datasets.
Dataset	Source File	Rows	Columns	Purpose
Customers	olist_customers_dataset.csv	99,441	5	Customer information
Geolocation	olist_geolocation_dataset.csv	1,000,163	5	Geographic information
Order Items	olist_order_items_dataset.csv	112,650	7	Products purchased in orders
Payments	olist_order_payments_dataset.csv	103,886	5	Payment information
Reviews	olist_order_reviews_dataset.csv	99,224	7	Customer reviews
Orders	olist_orders_dataset.csv	99,441	8	Order lifecycle
Products	olist_products_dataset.csv	32,951	9	Product information
Sellers	olist_sellers_dataset.csv	3,095	4	Seller information
Category Translation	product_category_name_translation.csv	71	2	Category translation

The row counts across the nine files should not be added together to represent the number of transactions.

Each dataset represents a different business entity, and several tables have one-to-many relationships.

For example, one order can contain multiple order items and can have multiple payment records.
8. High-Level Data Model

The order entity is central to the dataset.

The major relationships are:

Customers
    |
    | customer_id
    v
Orders
    |
    +--------------------+
    |                    |
    | order_id           | order_id
    v                    v
Order Items          Payments
    |
    +--------------------+
    |                    |
    | product_id         | seller_id
    v                    v
Products              Sellers

Reviews are associated with orders:

Orders
   |
   | order_id
   v
Reviews

Products can be associated with category translations:

Products
   |
   | product_category_name
   v
Category Translation

Customer and seller ZIP prefixes can be associated with geolocation information.

However, I did not treat the ZIP prefix as a unique geolocation key because the source contains multiple geographic observations for the same ZIP prefix.
9. ETL Architecture
9.1 Raw Data Layer

The original CSV files are stored under:

data/raw/

I keep the raw files unchanged.

This is an important design decision because it provides a reproducible source layer.

If I later change a transformation rule, I can regenerate the processed dataset from the original raw files.
9.2 Extraction Layer

The extraction layer reads the raw source files and performs basic validation.

Current extraction files include:

src/extraction/
    extract_data.py
    expected_columns.py
    validate_data.py

The extraction layer checks:

    File existence

    CSV readability

    Empty datasets

    Expected columns

    Basic source structure

9.3 Transformation Layer

The transformation layer prepares the extracted data for database loading.

The main activities include:

    Identifier standardization

    Date parsing

    Text normalization

    Column-name correction

    Missing-value handling

    Exact duplicate removal where justified

    Business-key validation

Processed datasets are stored under:

data/processed/

9.4 Loading Layer

The loading layer transfers the processed datasets into PostgreSQL.

Current loading components are stored under:

src/loading/

Database credentials are supplied through environment variables rather than hard-coded into Python scripts.
9.5 Validation Layer

I validate the data at several stages:

Source Validation
        |
        v
Transformation Validation
        |
        v
Processed Dataset Validation
        |
        v
Database Row Count Validation
        |
        v
Foreign-Key Validation
        |
        v
Primary / Composite-Key Validation

This staged validation makes it easier to identify exactly where an issue occurs.
10. Sprint 1: Requirements and Extraction
Sprint Objective

The objective of Sprint 1 was to understand the source data and establish a reliable extraction layer.

I deliberately started with profiling instead of immediately transforming the data.

The reasoning was simple:

Understand the data
        ↓
Identify risks
        ↓
Define transformation rules
        ↓
Implement transformations

11. August 10, 2026
Focus: Source Understanding and Initial Profiling

I began by examining all nine Olist CSV files.

I reviewed:

    Number of rows

    Number of columns

    Column names

    Data types

    Null values

    Duplicate values

    Candidate keys

    Relationships

    Orphan records

    Potential data-quality issues

I also began building the project data dictionary.
Initial Data Quality Investigation

Several findings required additional investigation.
Reviews

I found that:

review_id

was not unique.

There were:

814 duplicate review_id values

I also found:

551 duplicate order_id values

Instead of immediately deleting these records, I investigated the relationship between the two columns.

The combination:

(review_id, order_id)

was unique.

This showed that repeated individual identifiers did not necessarily mean duplicate records.
Decision

I decided to use the composite key:

(review_id, order_id)

for the database design.
Geolocation

The geolocation dataset contained:

1,000,163 rows

I identified:

261,836 exact duplicate rows

However, I also found that ZIP prefixes were frequently repeated.

This required distinguishing:

Exact duplicate row

from:

Multiple valid observations for the same ZIP prefix

Decision

I decided to remove only exact duplicate rows and preserve repeated ZIP prefixes.
Challenge

The main challenge on this date was determining whether repeated values represented actual duplicate records or legitimate business relationships.
How I Tackled It

I investigated the uniqueness of candidate keys and composite keys instead of relying only on a generic duplicate count.

This helped me avoid deleting potentially valid records.
Outcome

By the end of the initial profiling stage, I had a clearer understanding of:

    Dataset structure

    Candidate keys

    Relationships

    Null patterns

    Duplicate patterns

    Geolocation behavior

    Review identifier behavior

12. August 11, 2026
Focus: Extraction Layer

I began implementing the extraction layer.

The following files were created:

src/extraction/extract_data.py
src/extraction/expected_columns.py
src/extraction/validate_data.py

The extraction process was designed to perform basic source validation before allowing data to proceed.
Validation Checks

I implemented checks for:
File existence

The pipeline verifies that the expected source file is present.
Empty dataset

The pipeline checks whether the source file contains usable records.
Expected columns

Each dataset is checked against its expected schema.
CSV readability

The extraction process verifies that the CSV can be read successfully.
Challenge

Because there are nine different datasets, each with a different schema, one generic column definition would not be appropriate.
Resolution

I maintained expected columns separately for each dataset.

This makes the validation process explicit and easier to maintain.
Outcome

The extraction layer could now identify basic source problems before transformation begins.
13. August 12, 2026
Focus: Extraction Refinement and Validation

I refined the extraction process and tested it across all nine datasets.

The following checks were confirmed:

    File exists

    File can be read

    Dataset is not empty

    Expected columns are present

    Source structure is valid

All nine source files passed the extraction validation.
Challenge

I needed to make sure the extraction stage would fail early if a source file was missing or structurally different.
Resolution

I strengthened the validation checks before the transformation stage.
Outcome

The extraction layer was ready to act as the controlled entry point into the ETL pipeline.
14. August 13, 2026
Focus: Sprint 1 Completion

I reviewed the work completed during Sprint 1 and confirmed that the source layer was ready for transformation.
Completed

    Source profiling

    Null analysis

    Duplicate analysis

    Key analysis

    Relationship analysis

    Orphan checks

    Review investigation

    Geolocation investigation

    Data dictionary

    Extraction implementation

    Expected-column validation

    File existence validation

    Empty-dataset validation

    Extraction testing

Deferred

Extraction logging was not implemented at this stage.

I intentionally deferred logging until the automation and testing stage so that I could first complete the core ETL functionality.
15. Sprint 1 Challenges and Resolutions
Challenge	Investigation	Resolution
Repeated review IDs	Checked composite uniqueness	Used (review_id, order_id)
Repeated geolocation ZIP prefixes	Checked exact row duplication	Preserved repeated ZIP prefixes
Exact geolocation duplicates	Compared complete rows	Removed exact duplicates
Missing source files	Considered pipeline failure scenario	Added file existence validation
Empty source files	Considered invalid input scenario	Added empty-data validation
Schema changes	Compared expected and actual columns	Added expected-column validation
16. Sprint 1 Outcome

Sprint 1 established a validated source layer.

At this point, I had:

Raw Olist Data
      ↓
Source Profiling
      ↓
Data Quality Understanding
      ↓
Extraction
      ↓
Source Validation

The raw data remained unchanged.
17. Sprint 2: Transformation and Data Quality
Sprint Objective

The objective of Sprint 2 was to convert the raw source datasets into standardized, processed datasets that could safely be loaded into PostgreSQL.

I followed a conservative transformation strategy.

The goal was not to remove every null or repeated value.

The goal was to understand the business meaning of the data and transform it without destroying useful information.
18. Transformation Principles
Principle 1: Preserve Raw Data

I never modify files under:

data/raw/

All changes are made in the processed layer.
Principle 2: Do Not Remove Nulls Blindly

A missing value may represent a legitimate business condition.

For example:

Missing delivery date

may mean that the order has not yet reached that stage.

Similarly:

Missing review message

may mean that the customer submitted a rating without written feedback.
Principle 3: Remove Only Justified Duplicates

I remove exact duplicates only where there is sufficient evidence that they do not represent distinct business records.
Principle 4: Preserve Relationships

Transformations must not break relationships between customers, orders, products, sellers, payments, and reviews.
Principle 5: Standardize Data Types

Identifiers, dates, timestamps, text, and numeric values should have predictable formats before database loading.
19. Customer Transformation
Source

olist_customers_dataset.csv

Transformations

I:

    Standardized customer identifiers as strings.

    Normalized city text.

    Standardized state values.

    Preserved customer_id.

    Preserved customer_unique_id.

Important Decision

customer_unique_id contains repeated values.

I did not treat these repeated values as duplicate customer records.

The order relationship is based on:

customer_id

20. Order Transformation
Source

olist_orders_dataset.csv

Transformations

I:

    Converted order_id to string.

    Converted customer_id to string.

    Standardized order_status.

    Parsed date and timestamp fields.

    Preserved missing dates.

Important Decision

I did not fill missing dates with artificial values.

For example:

Missing delivery date

is different from:

Invalid delivery date

Preserving the null allows the later analytical layer to interpret the order lifecycle correctly.
21. Order Item Transformation
Source

olist_order_items_dataset.csv

Transformations

I:

    Standardized order_id.

    Standardized product_id.

    Standardized seller_id.

    Converted shipping_limit_date.

    Preserved order_item_id.

Database Key

I used:

(order_id, order_item_id)

as the composite primary key.

This represents the item sequence within each order.
22. Payment Transformation
Source

olist_order_payments_dataset.csv

Transformations

I:

    Standardized order_id.

    Converted payment_type to lowercase.

    Preserved payment sequence.

    Preserved installment information.

    Preserved payment value.

Database Key

I used:

(order_id, payment_sequential)

as the composite primary key.
23. Review Transformation
Source

olist_order_reviews_dataset.csv

Transformations

I:

    Standardized review_id.

    Standardized order_id.

    Parsed review dates.

    Preserved review scores.

    Preserved optional review title and message fields.

Key Decision

The source contains repeated individual review_id and order_id values.

After investigation, I confirmed that:

(review_id, order_id)

is unique.

Therefore, I did not remove records merely because one of the individual identifiers was repeated.
24. Product Transformation
Source

olist_products_dataset.csv

Transformations

I:

    Standardized product_id.

    Normalized category text.

    Corrected source column names.

    Preserved product dimensions.

    Preserved product weight.

    Preserved photo count.

    Preserved meaningful null values.

Column Corrections

The source contained:

product_name_lenght
product_description_lenght

I corrected these in the processed dataset to:

product_name_length
product_description_length

The raw source remains unchanged.
25. Seller Transformation
Source

olist_sellers_dataset.csv

Transformations

I:

    Standardized seller_id.

    Normalized city text.

    Standardized state values.

    Preserved seller ZIP prefix.

No major null-value problem was identified in this dataset.
26. Geolocation Transformation
Source

olist_geolocation_dataset.csv

Initial Size

1,000,163 rows

Data Quality Issue

I identified:

261,836 exact duplicate rows

Transformation

I removed exact duplicate rows.
Result

738,327 processed rows

Important Decision

I did not remove repeated ZIP prefixes.

A ZIP prefix can have multiple geographic observations.

Therefore:

ZIP prefix
    |
    +-- observation 1
    +-- observation 2
    +-- observation 3

can be valid.
Database Design

I therefore created a generated:

geolocation_id

as the PostgreSQL primary key.
27. Category Translation Transformation
Source

product_category_name_translation.csv

Transformations

I:

    Trimmed text values.

    Normalized category names.

    Preserved original category names.

    Preserved English translations.

28. Sprint 2 Validation

After transformation, I validated the processed datasets.
Dataset	Rows	Null Values Reported	Duplicate Business Key
Customers	99,441	0	0
Orders	99,441	4,908	0
Order Items	112,650	0	0
Payments	103,886	0	0
Reviews	99,224	145,903	0
Products	32,951	2,448	0
Sellers	3,095	0	0
Geolocation	738,327	0	Not applicable
Category Translation	71	0	0

The reported null values in Orders, Reviews, and Products are known source-level missing values.

I did not treat them as transformation failures.
29. Sprint 2 Challenges and Resolutions
Challenge 1: Meaningful Null Values
Problem

Several datasets contained missing values.
Risk

Blindly using:

dropna()

could remove valid business records.

Blindly using:

fillna(0)

could create incorrect business values.
Resolution

I evaluated nulls according to the meaning of each field.
Challenge 2: Geolocation Duplicates
Problem

The raw geolocation dataset contained 261,836 exact duplicates.

At the same time, ZIP prefixes were not unique.
Risk

Removing all repeated ZIP prefixes would remove potentially valid observations.
Resolution

I removed only exact duplicate rows.
Challenge 3: Product Column Names
Problem

The source contained spelling inconsistencies in column names.
Resolution

I corrected the names in the processed dataset while keeping the raw file unchanged.
Challenge 4: Review Identifier Repetition
Problem

Individual review identifiers were repeated.
Investigation

I checked the composite identifier.
Resolution

The combination (review_id, order_id) was unique, so I retained the records and used the composite key.
30. August 16, 2026
Focus: Transformation Finalization

I completed the transformation of all nine Olist datasets.
Completed

    All nine datasets transformed.

    Processed datasets generated.

    Identifiers standardized.

    Text fields standardized.

    Date fields parsed.

    Product column names corrected.

    Meaningful nulls preserved.

    Exact geolocation duplicates removed.

    Repeated ZIP prefixes preserved.

    Business keys validated.

    Data-quality checks completed.

Validation Result

All nine processed datasets passed the current transformation and data-quality validation checks.
31. August 17, 2026
Focus: Final Transformation Validation

I reviewed the processed datasets and confirmed that they were ready for database loading.

The transformation stage was considered complete after verifying:

    Expected row counts

    Expected columns

    Business-key uniqueness

    Data types

    Known null values

    Geolocation duplicate handling

    Product column naming

    Relationship compatibility

Outcome

The processed datasets became the input layer for PostgreSQL.
32. Sprint 2 Outcome

The transformation stage produced:

Raw Data
   |
   v
Transformed Data
   |
   +-- Standardized identifiers
   +-- Parsed dates
   +-- Standardized text
   +-- Corrected column names
   +-- Preserved meaningful nulls
   +-- Removed justified exact duplicates
   +-- Validated business keys

The processed datasets were ready for database loading.
33. Sprint 3: PostgreSQL and Data Loading
Sprint Objective

The objective of Sprint 3 is to create the PostgreSQL target database, define the relational schema, load the processed datasets, and validate the resulting database.
34. August 18, 2026
Focus: PostgreSQL Setup

I installed and configured PostgreSQL 18 on Windows.

The installation included:

    PostgreSQL server

    pgAdmin 4

    Command-line tools

The local server was configured with:

Host: localhost
Port: 5432
Username: postgres

35. Database Creation

I created a PostgreSQL database named:

ecommerce

The database is the target system for the processed Olist data.
36. Environment Configuration

Database credentials are stored using environment variables.

The .env structure is:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

The .env file is excluded from Git.

This prevents database credentials from being committed to the repository.
37. Python PostgreSQL Connection

I implemented the database configuration in:

src/loading/db_config.py

The Python ETL code uses:

psycopg

to connect to PostgreSQL.

The connection test returned:

PostgreSQL connection successful
Database: ecommerce

This confirmed that the Python loading layer could communicate successfully with the database.
38. PostgreSQL Schema

I created nine PostgreSQL tables:

category_translation
customers
geolocation
order_items
orders
payments
products
reviews
sellers

The schema is defined in:

sql/schema.sql

39. Primary Keys

The following keys were defined:
Table	Primary Key
customers	customer_id
sellers	seller_id
products	product_id
category_translation	product_category_name
orders	order_id
order_items	(order_id, order_item_id)
payments	(order_id, payment_sequential)
reviews	(review_id, order_id)
geolocation	Generated geolocation_id

The key design is based on the uniqueness checks performed during profiling.
40. Foreign Keys

I defined the main relational dependencies:

customers.customer_id
        |
        v
orders.customer_id

orders.order_id
        |
        +--> order_items.order_id
        +--> payments.order_id
        +--> reviews.order_id

products.product_id
        |
        v
order_items.product_id

sellers.seller_id
        |
        v
order_items.seller_id

These constraints provide database-level protection for referential integrity.
41. Why Geolocation Uses a Surrogate Key

The geolocation ZIP prefix is not unique.

Therefore, I did not define:

geolocation_zip_code_prefix

as the primary key.

Instead, I created:

geolocation_id BIGINT GENERATED ALWAYS AS IDENTITY

as the database key.

The original ZIP prefix remains available as a business attribute.

This design allows multiple valid observations to share the same ZIP prefix.
42. Data Loading

I created reusable Python loading functionality under:

src/loading/

The loader:

    Reads a processed CSV.

    Converts Pandas missing values into database-compatible NULL values.

    Connects to PostgreSQL.

    Inserts the records into the appropriate table.

    Commits the transaction.

    Reports the number of rows loaded.

43. Initial Database Load Results

All nine processed datasets were successfully loaded.
Table	Loaded Rows
customers	99,441
orders	99,441
order_items	112,650
payments	103,886
reviews	99,224
products	32,951
sellers	3,095
geolocation	738,327
category_translation	71

The database row counts match the processed dataset counts.
44. PostgreSQL Loading Blocker 1: Timestamp Datatype Mismatch
Problem

While loading the Orders dataset, PostgreSQL returned an error similar to:

column "order_delivered_carrier_date" is of type timestamp without time zone
but expression is of type double precision

Investigation

The source data was being read with Pandas.

Missing datetime values were represented as:

NaN

Pandas can use floating-point NaN to represent missing values.

PostgreSQL, however, expects:

NULL

for a missing database value.

The mismatch occurred at the Python-to-PostgreSQL boundary.
Resolution

Before insertion, I converted Pandas missing values to Python None:

data = data.astype(object).where(pd.notna(data), None)

This allows psycopg to send the missing value as SQL NULL.
Result

The Orders dataset loaded successfully after the change.
Lesson

This issue demonstrated that ETL pipelines must explicitly handle data-type conversion between different systems.

A value that represents missing data correctly in Pandas does not necessarily map automatically to the correct PostgreSQL representation.
45. PostgreSQL Loading Blocker 2: Duplicate Product Primary Key
Problem

A later Products load produced:

duplicate key value violates unique constraint "products_pkey"

The error indicated that a product_id already existed.
Investigation

The Products dataset had already been loaded successfully.

The loading script was executed again for the same dataset.

Because:

products.product_id

is the primary key, PostgreSQL correctly rejected the second insertion.
Resolution

I stopped the repeated load instead of attempting to bypass the primary-key constraint.

The incident also identified a future improvement:

The loading process should support controlled repeat execution.

A production pipeline could use techniques such as staging tables, controlled truncation, or conflict-handling strategies depending on the desired loading model.

I am not marking those features as implemented until they are actually added to the project.
46. PostgreSQL Loading Blocker 3: Geolocation Performance
Problem

The geolocation dataset contains:

738,327 processed rows

A normal row-by-row insertion approach is inefficient for this volume.
Investigation

I recognized that the loading method should depend on the dataset size.

Using the same insertion strategy for every dataset would make the large geolocation load unnecessarily slow.
Resolution

I created a dedicated loader:

src/loading/load_geolocation.py

It uses PostgreSQL:

COPY

for bulk loading.
Result

The complete geolocation dataset was loaded successfully.
47. Database Row Count Validation

After loading the data, I compared the PostgreSQL row counts with the processed CSV row counts.

The results matched for all nine tables.

This confirms that the expected number of processed records reached the database.
48. Foreign-Key Validation

I also checked the major relationships for orphan records.

Results:

Customers -> Orders: 0
Orders -> Order Items: 0
Orders -> Payments: 0
Orders -> Reviews: 0
Products -> Order Items: 0
Sellers -> Order Items: 0

All tested relationships returned zero orphan records.

This confirms that the loaded records currently maintain the expected referential relationships.
49. Remaining Database Validation

The final primary-key and composite-key validation is still pending.

I will validate:

    customer_id

    order_id

    product_id

    seller_id

    product_category_name

    (order_id, order_item_id)

    (order_id, payment_sequential)

    (review_id, order_id)

The documentation will be updated after these checks are actually executed.
50. Sprint 3 Challenge Summary
Challenge	Cause	Resolution	Status
Timestamp datatype mismatch	Pandas NaN reached PostgreSQL timestamp fields	Converted missing values to Python None	Resolved
Duplicate product primary key	Products were loaded more than once	Stopped repeated load and identified need for repeat-safe loading	Resolved for current run
Geolocation performance	738K+ records made row-by-row loading inefficient	Used PostgreSQL COPY	Resolved
Final key validation	Final database key checks remain	Execute primary/composite-key validation	Pending
51. Current Data Quality Findings
Customers

    customer_id is unique.

    customer_unique_id contains repeated values.

    Repeated customer_unique_id values were not treated as duplicate customer records.

    The customer-order relationship uses customer_id.

Orders

    Some approval and delivery timestamps are missing.

    Missing dates were preserved.

    order_id is unique.

Order Items

    Multiple items can belong to one order.

    (order_id, order_item_id) is used as the composite key.

Payments

    Multiple payment records can belong to one order.

    (order_id, payment_sequential) is used as the composite key.

Reviews

    Individual review_id values can repeat.

    Individual order_id values can repeat.

    (review_id, order_id) is unique.

    Review text fields contain many null values.

Products

    Several product attributes contain missing values.

    Product category and descriptive attributes have missing values.

    Source column spelling inconsistencies were corrected.

Sellers

    Seller identifiers are clean.

    No significant null-value issue was identified.

Geolocation

    Raw dataset contains 261,836 exact duplicate rows.

    ZIP prefix is not unique.

    Multiple observations can exist for the same ZIP prefix.

    Exact duplicates were removed.

    Processed dataset contains 738,327 rows.

52. Relationship Validation Reference
Parent	Child	Key	Orphan Records
Customers	Orders	customer_id	0
Orders	Order Items	order_id	0
Products	Order Items	product_id	0
Sellers	Order Items	seller_id	0
Orders	Payments	order_id	0
Orders	Reviews	order_id	0

An orphan record is a child record that refers to a parent record that does not exist.

Example:

Order Item
order_id = ABC123
       |
       v
Orders
order_id = ABC123

This is valid.

If ABC123 does not exist in the Orders table, the Order Item would be an orphan.

No orphan records were found in the tested relationships.
53. Source Data Dictionary
53.1 Customers

File: olist_customers_dataset.csv

Rows: 99,441
Column	Meaning
customer_id	Customer record identifier
customer_unique_id	Underlying customer identifier
customer_zip_code_prefix	Customer ZIP prefix
customer_city	Customer city
customer_state	Customer state

Primary Key:

customer_id

Relationship:

customers.customer_id
        |
        v
orders.customer_id

54. Orders

File: olist_orders_dataset.csv

Rows: 99,441
Column	Meaning
order_id	Order identifier
customer_id	Customer associated with the order
order_status	Order status
order_purchase_timestamp	Purchase timestamp
order_approved_at	Approval timestamp
order_delivered_carrier_date	Carrier delivery date
order_delivered_customer_date	Customer delivery date
order_estimated_delivery_date	Estimated delivery date

Primary Key:

order_id

55. Order Items

File: olist_order_items_dataset.csv

Rows: 112,650
Column	Meaning
order_id	Associated order
order_item_id	Item sequence within order
product_id	Purchased product
seller_id	Seller
shipping_limit_date	Shipping deadline
price	Item price
freight_value	Freight amount

Primary Key:

(order_id, order_item_id)

56. Payments

File: olist_order_payments_dataset.csv

Rows: 103,886
Column	Meaning
order_id	Associated order
payment_sequential	Payment sequence
payment_type	Payment method
payment_installments	Number of installments
payment_value	Payment amount

Primary Key:

(order_id, payment_sequential)

57. Reviews

File: olist_order_reviews_dataset.csv

Rows: 99,224
Column	Meaning
review_id	Review identifier
order_id	Associated order
review_score	Review score
review_comment_title	Review title
review_comment_message	Review message
review_creation_date	Review creation date
review_answer_timestamp	Review answer timestamp

Primary Key:

(review_id, order_id)

58. Products

File: olist_products_dataset.csv

Rows: 32,951
Column	Meaning
product_id	Product identifier
product_category_name	Product category
product_name_length	Product name length
product_description_length	Product description length
product_photos_qty	Number of photos
product_weight_g	Product weight
product_length_cm	Product length
product_height_cm	Product height
product_width_cm	Product width
59. Sellers

File: olist_sellers_dataset.csv

Rows: 3,095
Column	Meaning
seller_id	Seller identifier
seller_zip_code_prefix	Seller ZIP prefix
seller_city	Seller city
seller_state	Seller state

Primary Key:

seller_id

60. Geolocation

File: olist_geolocation_dataset.csv

Raw Rows: 1,000,163

Processed Rows: 738,327
Column	Meaning
geolocation_zip_code_prefix	ZIP prefix
geolocation_lat	Latitude
geolocation_lng	Longitude
geolocation_city	City
geolocation_state	State

Database Primary Key:

geolocation_id

The ZIP prefix remains a business attribute and is not treated as unique.
61. Category Translation

File: product_category_name_translation.csv

Rows: 71
Column	Meaning
product_category_name	Original category
product_category_name_english	English category

Primary Key:

product_category_name

62. PostgreSQL Schema Reference

The target database contains:

ecommerce
|
+-- customers
|
+-- orders
|
+-- order_items
|
+-- payments
|
+-- reviews
|
+-- products
|
+-- sellers
|
+-- geolocation
|
+-- category_translation

The schema is defined in:

sql/schema.sql

63. Project Structure

Ecommerce/
|
+-- data/
|   +-- raw/
|   |   +-- Olist CSV files
|   |
|   +-- processed/
|       +-- transformed CSV files
|
+-- docs/
|   +-- 06_data_dictionary.md
|   +-- 07_transformation_rules.md
|
+-- sql/
|   +-- schema.sql
|
+-- src/
|   +-- extraction/
|   |   +-- extract_data.py
|   |   +-- expected_columns.py
|   |   +-- validate_data.py
|   |
|   +-- profiling/
|   |
|   +-- transformation/
|   |   +-- transformation scripts
|   |   +-- validate_all.py
|   |
|   +-- loading/
|       +-- db_config.py
|       +-- test_connection.py
|       +-- load_data.py
|       +-- load_geolocation.py
|
+-- .env
+-- .gitignore

64. Git and Repository Practices

I am using Git throughout the project to maintain development history.

The project uses feature branches instead of making development changes directly on main.

Current branches include:

main
develop
feature/extraction
feature/transformation

The purpose is to keep development changes organized and allow me to maintain stable branches.

The raw data directory is excluded from Git because the source files can be large.

The .env file is also excluded because it contains database credentials.
65. Important Engineering Decisions
65.1 Raw Data Is Never Modified

I keep the source files unchanged.

All transformation work occurs in:

data/processed/

This gives me a reproducible ETL process.
65.2 Nulls Are Evaluated Based on Meaning

I do not automatically remove or replace missing values.

A null value can represent a valid business state.
65.3 Exact Duplicates and Repeated Keys Are Different

I distinguish between:

Exact duplicate row

and:

Repeated identifier

The review and geolocation datasets demonstrated why this distinction is important.
65.4 Composite Keys Are Used When Required

I use composite keys where a single source field cannot uniquely identify a record.

Examples:

(order_id, order_item_id)
(order_id, payment_sequential)
(review_id, order_id)

65.5 ZIP Prefix Is Not a Unique Geolocation Key

The geolocation dataset contains multiple records for the same ZIP prefix.

Therefore, I use a generated database identifier instead.
65.6 PostgreSQL Is the Target Database

I selected PostgreSQL because it provides:

    Relational integrity

    Primary-key constraints

    Foreign-key constraints

    Composite-key support

    Strong SQL capabilities

    Support for analytical workloads

    Efficient bulk loading

66. Lessons Learned
Lesson 1: Profile Before Transforming

I learned that transformation decisions should be based on actual source behavior.

The review and geolocation investigations demonstrated why profiling is important.
Lesson 2: Data Quality Requires Context

A duplicate value does not necessarily mean a duplicate record.

A null value does not necessarily mean bad data.

Both need to be evaluated in context.
Lesson 3: Different Systems Represent Missing Data Differently

The timestamp loading issue demonstrated that Pandas and PostgreSQL do not necessarily represent missing values in the same way.

This needs to be handled explicitly at system boundaries.
Lesson 4: Database Constraints Are Useful Validation Tools

The duplicate product loading issue showed how PostgreSQL constraints can detect problems that may otherwise go unnoticed.
Lesson 5: Loading Strategy Should Depend on Data Size

The geolocation dataset demonstrated that large tables may require a more efficient loading mechanism such as PostgreSQL COPY.
Lesson 6: ETL Pipelines Should Eventually Be Repeatable

The duplicate product load highlighted the importance of designing a production pipeline so that rerunning a stage does not unintentionally duplicate records.
67. Current Project Status
Sprint 1

Status: Completed

I completed:

    Source understanding

    Source profiling

    Null analysis

    Duplicate analysis

    Key analysis

    Relationship analysis

    Orphan checks

    Review investigation

    Geolocation investigation

    Data dictionary

    Extraction implementation

    Expected schema validation

    File validation

    Empty dataset validation

    Extraction testing

Sprint 2

Status: Completed

I completed:

    Transformation of all nine datasets

    Identifier standardization

    Date conversion

    Text standardization

    Product column correction

    Geolocation duplicate handling

    Data-quality validation

    Business-key validation

    Processed dataset generation

Sprint 3

Status: In Progress

I completed:

    PostgreSQL 18 installation

    PostgreSQL configuration

    ecommerce database creation

    Nine-table schema

    Primary-key definitions

    Foreign-key definitions

    Python database connection

    Loading of all nine datasets

    Row-count validation

    Foreign-key/orphan validation

    Geolocation bulk loading

Remaining

    Primary-key validation

    Composite-key validation

    Additional database checks

    SQL validation queries

    Final Sprint 3 documentation

68. Upcoming Work
Remaining Sprint 3 Work

I will:

    Complete primary-key validation.

    Complete composite-key validation.

    Run additional database quality checks.

    Review the loading scripts.

    Document the final database validation results.

69. Sprint 4: Automation and Testing

The next major stage will be connecting the individual ETL components.

The intended workflow is:

Extraction
    |
    v
Source Validation
    |
    v
Transformation
    |
    v
Transformation Validation
    |
    v
PostgreSQL Loading
    |
    v
Database Validation

I also plan to add:

    Logging

    Failure handling

    Controlled repeat execution

    End-to-end testing

    Final data-quality validation

70. Future Automation Design

The current Olist dataset is a static historical dataset.

Therefore, I am implementing it as a batch ETL pipeline rather than a real-time streaming system.

Automation does not require real-time data.

A future automated version can execute the same pipeline whenever a new source batch becomes available.

The conceptual workflow is:

Scheduler
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
PostgreSQL Load
    |
    v
Database Validation
    |
    v
Logging / Monitoring

For this project, automation can initially be demonstrated with a scheduler such as Windows Task Scheduler.

A production environment could use a workflow orchestration platform such as Airflow, but I will only claim a technology as implemented if I actually use it in the project.
71. Potential Automated Pipeline Failures
Missing Source File

If a source file is missing:

Stop pipeline
    ↓
Record failure
    ↓
Notify / report failure

Unexpected Schema

If the source columns change:

Source validation fails
    ↓
Transformation does not start
    ↓
Problem is recorded

Invalid Data

If data-quality validation fails:

Stop affected stage
    ↓
Record validation issue
    ↓
Prevent bad data from reaching PostgreSQL

Database Connection Failure

The pipeline should eventually:

Attempt connection
    ↓
Retry if appropriate
    ↓
Log failure if connection remains unavailable

Duplicate Records

Business keys and database constraints should prevent unintended duplicate loads.
Partial Pipeline Failure

The pipeline should eventually identify which stage completed successfully so that I can restart from a controlled point without unnecessarily duplicating previous work.
72. Project Development Philosophy

The main principle I am following is:

Do not simply make the data work.
Understand why it behaves the way it does.

For each issue I encounter, I try to follow this process:

Identify
   ↓
Investigate
   ↓
Understand the cause
   ↓
Choose a suitable solution
   ↓
Implement
   ↓
Validate
   ↓
Document

This approach is particularly important in ETL because blindly fixing errors can introduce incorrect business data.
73. Final ETL Design

The intended final architecture is:

                    OLIST SOURCE DATA
                           |
                           v
                    +--------------+
                    |  EXTRACTION  |
                    +--------------+
                           |
                           v
                  +-------------------+
                  | SOURCE VALIDATION |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |  TRANSFORMATION   |
                  +-------------------+
                           |
                           v
                 +---------------------+
                 | DATA QUALITY CHECK  |
                 +---------------------+
                           |
                           v
                  +-------------------+
                  | POSTGRESQL LOAD   |
                  +-------------------+
                           |
                           v
                 +---------------------+
                 | DATABASE VALIDATION|
                 +---------------------+
                           |
                           v
                  +-------------------+
                  | SQL / POWER BI    |
                  +-------------------+

74. Development Milestone Summary
Date	Sprint	Work Performed	Outcome
Aug 10	Sprint 1	Source profiling	Dataset structure and quality issues identified
Aug 11	Sprint 1	Extraction implementation	Source validation created
Aug 12	Sprint 1	Extraction refinement	All nine source files validated
Aug 13	Sprint 1	Sprint completion	Source layer finalized
Aug 14	Sprint 2	Transformation setup	Transformation approach established
Aug 15	Sprint 2	Transformation	Dataset-level cleaning implemented
Aug 16	Sprint 2	Transformation finalization	All nine datasets transformed
Aug 17	Sprint 2	Final validation	Processed datasets validated
Aug 18	Sprint 3	PostgreSQL setup and loading	Database populated and relationships checked
Aug 19 onward	Sprint 3	Database validation	Remaining database validation

Future dates will only be updated after the corresponding work is actually completed.
75. Project Completion Criteria

The project will be considered complete when:
Source Layer

    All source files are available.

    Source schemas are validated.

    Raw files remain unchanged.

Transformation Layer

    All nine datasets are transformed.

    Transformation rules are documented.

    Business keys are validated.

    Data-quality checks pass.

Database Layer

    PostgreSQL schema is created.

    Primary keys are valid.

    Composite keys are valid.

    Foreign keys are valid.

    Row counts match processed datasets.

    No unexpected orphan records exist.

Pipeline Layer

    Extraction, transformation, and loading can run as a connected workflow.

    Failures are handled safely.

    Logging is implemented.

    Repeat execution is controlled.

Documentation Layer

    Data dictionary is complete.

    Transformation rules are documented.

    Database schema is documented.

    ETL architecture is documented.

    Development blockers and resolutions are recorded.

    Setup instructions are available.

76. Final Project Summary

This is a solo end-to-end ETL project built using the Olist Brazilian E-Commerce Public Dataset.

I started the project by understanding and profiling the source data rather than immediately modifying it.

During the first sprint, I investigated the structure of all nine datasets, identified relationships, analyzed missing values, investigated duplicate patterns, evaluated candidate keys, and built the extraction validation layer.

During the second sprint, I transformed all nine datasets. I standardized identifiers and text, parsed dates, corrected inconsistent product column names, preserved meaningful null values, and removed only justified exact duplicates from the geolocation dataset.

During the third sprint, I introduced PostgreSQL as the target database. I designed the relational schema, defined primary and composite keys, added foreign-key relationships, configured the Python database connection, and loaded all nine processed datasets.

The database loading stage presented several practical engineering challenges.

The first was a timestamp datatype mismatch caused by Pandas missing values being represented as NaN while PostgreSQL expected NULL. I resolved this by converting missing values to Python None before insertion.

The second was a duplicate product primary-key error caused by attempting to load an already populated Products table again. This demonstrated the importance of repeat-safe loading in a production ETL pipeline.

The third was the large size of the geolocation dataset. I addressed this by creating a dedicated loader using PostgreSQL COPY for efficient bulk loading.

After loading, I validated the row counts and checked the major foreign-key relationships. All nine datasets reached PostgreSQL with the expected row counts, and the tested relationships returned zero orphan records.

The project is currently in Sprint 3.

The remaining work is focused on final database key validation, additional SQL validation, pipeline integration, automation, testing, final documentation, and the analytics layer.

The project is being developed independently, so every technical decision, blocker, resolution, and validation result documented here represents my own implementation and investigation.
77. Quick Reference
Project

E-Commerce Orders & Customer Analytics ETL

Type

Solo End-to-End ETL Project

Dataset

Olist Brazilian E-Commerce Public Dataset

Language

Python

Database

PostgreSQL 18

Database Name

ecommerce

Host

localhost

Port

5432

Source Datasets

9

Processed Datasets

9

PostgreSQL Tables

9

Main ETL Directories

src/extraction/
src/profiling/
src/transformation/
src/loading/

Main Documentation

docs/06_data_dictionary.md
docs/07_transformation_rules.md

Current Database Row Counts

customers              99,441
orders                 99,441
order_items           112,650
payments              103,886
reviews                99,224
products               32,951
sellers                 3,095
geolocation           738,327
category_translation       71

Current Status

Sprint 1: Completed
Sprint 2: Completed
Sprint 3: In Progress
Sprint 4: Planned
Final Release: Planned

78. Documentation Update Format

As I continue developing the project, each new development day should be documented using the following structure:

## [Date]

### Sprint
Sprint number

### Objective
What I intended to accomplish.

### Work Completed
What I actually implemented.

### Findings
Important observations discovered during implementation.

### Blocker / Challenge
Any technical or data-quality issue encountered.

### Investigation
How I analyzed the problem.

### Resolution
What I changed to solve it.

### Validation
How I confirmed the solution worked.

### Outcome
What became possible after the work was completed.

### Next Step
What I will work on next.

This keeps the document chronological, technical, and useful as both a project record and a presentation document.
79. Final Documentation Principle

This document is intended to preserve the complete development history of the project.

It should answer five questions for every major stage:

What did I build?
        ↓
Why did I build it?
        ↓
What problem did I encounter?
        ↓
How did I solve it?
        ↓
How did I verify it worked?

The purpose is not only to describe the final ETL pipeline.

It also records the reasoning and troubleshooting involved in building it.

That makes the project easier to explain during technical interviews because I can describe not only the technologies I used, but also the actual engineering problems I encountered and how I solved them.
