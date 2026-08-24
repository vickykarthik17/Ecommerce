# Challenges and Solutions

## 1. Purpose

This document records the significant technical blockers encountered while building the Ecommerce ETL pipeline, how each problem was investigated, the root cause identified, the solution applied, and the lesson learned.

The goal is to show that the pipeline was developed through evidence-based debugging rather than by cleaning or modifying data arbitrarily.

---

# 2. Challenge: Understanding the Dataset Before Cleaning

## Problem

The project contains multiple related CSV datasets with different business roles.

A generic cleaning approach could easily remove valid records or incorrectly treat repeated identifiers as errors.

## Investigation

The datasets were profiled before deciding transformation rules.

Important questions included:

- What does each table represent?
- Which columns identify records?
- Which identifiers are actually unique?
- Which NULL values are legitimate?
- Which repeated values represent one-to-many relationships?
- Which fields will become database keys?
- Which values need to match PostgreSQL datatypes?

## Resolution

A business-context and profiling-first approach was followed:

```text
Business meaning
      ↓
Data profiling
      ↓
Identify actual data-quality issue
      ↓
Choose transformation
```

## Lesson

Data cleaning should be driven by business meaning and target-system requirements, not by appearance alone.

---

# 3. Challenge: Identifying Correct Keys

## Problem

Not every field ending in `_id` is globally unique.

Treating every ID column as a primary key would have produced an incorrect relational model.

## Investigation

The datasets were checked for duplicate identifiers.

This revealed cases where a record is identified by a combination of fields.

Examples:

```text
order_items
(order_id, order_item_id)
```

```text
payments
(order_id, payment_sequential)
```

```text
reviews
(review_id, order_id)
```

## Resolution

Composite keys were used where required.

This preserved legitimate records instead of deleting them simply because one identifier repeated.

## Lesson

Primary-key decisions must come from actual cardinality and business structure.

---

# 4. Challenge: Review Identifier Duplicates

## Problem

The review dataset contained repeated values for identifiers that initially appeared suitable as keys.

Simply dropping duplicate rows or selecting one row per review identifier could have removed legitimate review information.

## Investigation

The relationship between:

```text
review_id
```

and:

```text
order_id
```

was examined.

The combination was found to provide the required uniqueness for the database design.

## Resolution

The review table uses:

```text
(review_id, order_id)
```

as the composite primary key.

## Lesson

A repeated identifier does not automatically mean duplicate data.

The surrounding business relationship must be considered.

---

# 5. Challenge: Geolocation Duplicate Records

## Problem

The raw geolocation dataset contained:

```text
1,000,163 rows
```

There were many repeated geographical observations.

At first glance, removing them could appear to be arbitrary data loss.

## Investigation

The duplicate records were examined as exact duplicate observations.

The dataset represents geographical reference information rather than individual transactions.

## Resolution

Exact duplicate rows were removed.

The resulting processed dataset contains:

```text
738,327 rows
```

This means:

```text
1,000,163
-
738,327
=
261,836
```

duplicate rows were removed.

## Important Design Decision

`geolocation_zip_code_prefix` was not made the primary key because multiple geographical records can legitimately share a ZIP-code prefix.

A generated:

```text
geolocation_id
```

was therefore used as the database identifier.

## Lesson

Duplicate removal and key selection are separate decisions.

---

# 6. Challenge: Product Column Naming

## Problem

The product source contained column names with spelling issues:

```text
product_name_lenght
product_description_lenght
```

## Investigation

The intended business meaning of the columns was clear: they represent lengths associated with the product name and description.

## Resolution

The processed schema uses:

```text
product_name_length
product_description_length
```

## Lesson

Schema standardization improves readability and reduces confusion downstream.

---

# 7. Challenge: PostgreSQL Product Datatype Error

## Problem

During database loading, PostgreSQL rejected product data because values such as:

```text
40.0
```

were being loaded into integer-compatible fields.

The pipeline therefore failed at the database boundary.

## Error Type

The issue was a datatype mismatch between the processed CSV representation and the PostgreSQL schema.

## Investigation

The source data was examined and the target PostgreSQL column definitions were compared.

The values represented integer-compatible quantities, but Pandas had represented some values as floating-point because of the source data and missing-value behavior.

## Resolution

The relevant product fields were explicitly converted to integer-compatible values before loading.

Conceptually:

```text
40.0
```

became:

```text
40
```

## Lesson

CSV files are weakly typed compared with a relational database.

Target database datatypes must therefore be considered during transformation.

---

# 8. Challenge: Duplicate-Key Failure During Pipeline Rerun

## Problem

A rerun of the pipeline caused a PostgreSQL duplicate primary-key error.

The problem occurred because the same complete dataset was being inserted into tables that already contained the previous run's records.

Conceptually:

```text
Existing batch
     +
Same batch again
     ↓
Duplicate primary key
```

## Investigation

The error was traced to the database loading stage rather than extraction or transformation.

The dataset itself was not necessarily duplicated; the database already contained the previous batch.

## Resolution

The loading strategy was changed to a controlled full refresh:

```text
TRUNCATE existing tables
        ↓
Load processed CSVs
```

`CASCADE` was used where necessary to account for foreign-key dependencies.

## Lesson

For a static historical dataset, a full-refresh strategy is simpler and more appropriate than repeatedly inserting the same snapshot.

---

# 9. Challenge: Failed Orders Transformation Write

## Problem

During one pipeline run, the following error occurred while writing:

```text
data/processed/orders_clean.csv
```

The pipeline reported:

```text
OSError: [Errno 22] Invalid argument
```

The failure occurred inside:

```text
src/transformation/transform_orders.py
```

during:

```python
data.to_csv(output_file, index=False)
```

## Investigation

The failure was treated as a runtime/file-system issue because the traceback pointed to the file-writing operation rather than the transformation logic itself.

The pipeline's new error handling successfully captured the traceback and identified the exact failed step.

## Resolution

The issue was retried and the pipeline subsequently completed successfully, confirming that the transformation logic and output path were functioning normally afterward.

## Lesson

Centralized orchestration error handling is valuable even when the underlying failure is transient or environment-specific.

---

# 10. Challenge: Making Pipeline Failures Visible

## Problem

Before centralized logging and error handling, a failed subprocess could provide limited orchestration-level context.

It was not enough to know that the overall pipeline stopped.

## Resolution

`run_pipeline.py` was enhanced to:

```text
Capture stdout/stderr
        ↓
Check return code
        ↓
Log actual stderr
        ↓
Identify failed step
        ↓
Record execution time
        ↓
Stop the pipeline
```

Example:

```text
ERROR | Error output from src/transformation/transform_orders.py:
Traceback ...

ERROR | Pipeline failed at:
src/transformation/transform_orders.py
after 2.10 seconds
```

## Lesson

A pipeline should fail clearly rather than fail silently.

---

# 11. Challenge: Deciding Whether to Use Rotating Logs

## Problem

A rotating file handler was considered for log management.

The question was whether the project actually required automatic log rotation.

## Investigation

The project's characteristics were considered:

- Static historical dataset
- Batch ETL execution
- Project demonstration rather than continuously running production service
- No requirement for indefinite daily log retention

## Resolution

A standard:

```python
logging.FileHandler
```

was used.

A rotating handler was not added because it would introduce additional complexity without solving a current project requirement.

## Lesson

Engineering decisions should match project requirements rather than adding production infrastructure simply because it exists.

---

# 12. Challenge: Understanding Whether the Pipeline Should Run Daily

## Problem

The project contains a large dataset, which raised the question:

> If the same data is static, what is the purpose of running the pipeline every day?

## Investigation

The source was identified as a static historical Olist dataset.

It does not represent a live production feed receiving new orders every day.

## Resolution

The pipeline is treated as a repeatable batch ETL demonstration.

Repeated execution demonstrates:

```text
Reproducibility
Repeatability
Validation
Failure recovery
Database reconstruction
```

It does not claim to be a daily production ingestion system.

## Lesson

Scheduling is only useful when the source or business process changes over time.

---

# 13. Challenge: Choosing Full Refresh Instead of Incremental Loading

## Problem

A production-style ETL project might use incremental loading, but implementing it here would require assumptions about:

- New records
- Change timestamps
- Watermarks
- Upserts
- CDC
- Source availability

## Resolution

A full-refresh strategy was chosen because the source is a static historical snapshot.

```text
TRUNCATE
   ↓
COPY full processed dataset
   ↓
Validate
```

This provides deterministic repeatability without inventing incremental business rules.

## Lesson

The simplest architecture that correctly fits the source should be preferred.

---

# 14. Challenge: Handling Legitimate NULL Values

## Problem

The processed datasets contain NULL values.

For example:

```text
orders_clean.csv
NULL values: 4,908
```

and:

```text
reviews_clean.csv
NULL values: 145,903
```

Treating every NULL as an error would result in incorrect cleaning.

## Investigation

The business meaning of the affected columns was considered.

Examples include optional review text and order lifecycle timestamps that may not exist for every record.

## Resolution

NULLs were retained when they represented missing but legitimate information.

The validation layer reports NULL counts instead of blindly replacing them.

## Lesson

NULL is a data state, not automatically a data-quality failure.

---

# 15. Challenge: Preserving One-to-Many Relationships

## Problem

Several datasets contain repeated foreign keys.

For example:

```text
One order
   ↓
Multiple order items
```

and:

```text
One order
   ↓
Multiple payment records
```

Treating these repetitions as duplicates would destroy business information.

## Resolution

The original transactional granularity was preserved.

Composite keys were used where necessary.

## Lesson

Duplicate-looking values can represent legitimate one-to-many relationships.

---

# 16. Challenge: Validating at Multiple Stages

## Problem

Checking the database only after loading would make it harder to identify where a problem originated.

## Resolution

Validation was split into three layers:

```text
Source Validation
        ↓
Transformation Validation
        ↓
Database Validation
```

### Source Validation

Checks expected source files and columns.

### Transformation Validation

Checks:

- Row counts
- Column counts
- NULL counts
- Duplicate-key conditions

### Database Validation

Checks:

- Database row counts
- Keys
- Foreign keys
- Referential integrity

## Lesson

Multiple quality gates make failures easier to isolate.

---

# 17. Challenge: Testing Error Handling Instead of Assuming It Works

## Problem

Adding error-handling code does not prove that it behaves correctly.

## Resolution

A controlled failure test was used:

```text
src/test_failure.py
```

The failure path was exercised and verified to:

```text
Detect failure
     ↓
Capture error
     ↓
Log error
     ↓
Identify failed step
     ↓
Stop pipeline
```

The temporary failure was then removed and the normal pipeline was rerun.

## Lesson

Failure paths should be tested deliberately.

---

# 18. Challenge: Git Branch and Integration Management

## Problem

The project was developed through feature branches, including:

```text
feature/extraction
feature/transformation
develop
```

The challenge was ensuring that completed work was integrated into the development branch without leaving the repository in an inconsistent state.

## Resolution

The completed work was brought into `develop`.

The branch was checked with:

```powershell
git branch --show-current
```

and:

```powershell
git status
```

The local `develop` branch was then pushed to GitHub.

The final synchronization check:

```powershell
git log --oneline develop..origin/develop
```

returned no output, confirming that the remote `origin/develop` contained the same commits.

## Lesson

Branch status and remote synchronization should be explicitly verified before considering a milestone complete.

---

# 19. Challenge: Documentation Based on Actual Engineering Decisions

## Problem

Simply documenting what the code does would not explain why the implementation looks the way it does.

## Resolution

Documentation was structured around:

```text
Business Meaning
      ↓
Data Profiling
      ↓
Observed Problem
      ↓
Engineering Decision
      ↓
Implementation
      ↓
Validation
```

This explains decisions such as:

- Why geolocation duplicates were removed
- Why review records were not arbitrarily deduplicated
- Why composite keys were required
- Why NULLs were retained
- Why full refresh was selected
- Why PostgreSQL datatype conversion was required
- Why centralized logging was added

## Lesson

Good ETL documentation explains decisions and trade-offs, not just code syntax.

---

# 20. Challenge: Keeping the Scope Appropriate

## Problem

It was tempting to add features such as:

```text
Airflow
Docker orchestration
Kafka
Streaming ingestion
Cloud scheduling
Incremental CDC
Advanced monitoring
```

even though the current project did not require them.

## Resolution

The implementation was kept focused on:

```text
Extraction
Transformation
Validation
PostgreSQL Loading
Orchestration
Logging
Error Handling
Documentation
```

The architecture remains extensible without adding infrastructure that cannot be meaningfully demonstrated with the static source dataset.

## Lesson

A strong project is not necessarily the one with the most technologies. It is the one where each technology has a clear purpose.

---

# 21. Final Blocker-to-Solution Summary

| Blocker | Root Cause | Solution |
|---|---|---|
| Incorrect assumptions about duplicate IDs | IDs did not always represent global uniqueness | Profiling + composite keys |
| Review identifier repetition | One identifier was not sufficient | Composite `(review_id, order_id)` key |
| Geolocation duplicates | Repeated exact observations | Exact duplicate removal |
| ZIP prefix not unique | Multiple geographical observations per prefix | Surrogate `geolocation_id` |
| Product column spelling | Source naming inconsistency | Standardized column names |
| PostgreSQL product datatype error | CSV/Pandas numeric representation differed from target schema | Explicit datatype conversion |
| Duplicate key during rerun | Previous batch remained in database | Full refresh with `TRUNCATE ... CASCADE` |
| Orders CSV write error | File-writing/runtime failure | Captured traceback, retried, verified successful execution |
| Limited failure visibility | Subprocess errors were not centrally tracked | Centralized logging + stderr capture |
| Question of daily execution | Source is static historical data | Repeatable batch model |
| Log rotation question | No continuous production log requirement | Standard `FileHandler` |
| NULL values | Some missing values have legitimate meaning | Profile + retain valid NULLs |
| Validation uncertainty | One validation layer could not isolate all failures | Source + transformation + database validation |
| Error-handling confidence | Failure path was not automatically proven | Controlled failure test |
| Git integration | Work existed across branches | Explicit branch/status/remote verification |
| Documentation gaps | Code alone did not explain decisions | Decision-based documentation |

---

# 22. Key Engineering Lessons

The major lessons from the project are:

### 1. Profile before transforming

```text
Understand
   ↓
Profile
   ↓
Transform
```

not:

```text
Clean everything
   ↓
Hope nothing important was removed
```

### 2. Business meaning determines data quality rules

A repeated identifier may be:

```text
Invalid duplicate
```

or:

```text
Valid one-to-many relationship
```

The business context determines which one it is.

### 3. Target schema matters

Transformation is not only about cleaning source data.

It also prepares data for the target database.

### 4. NULL does not automatically mean bad data

Missing values must be interpreted according to the field's meaning.

### 5. Validation should be layered

```text
Source
   ↓
Processed
   ↓
Database
```

### 6. Errors should be reproducible and traceable

The pipeline should clearly answer:

```text
What failed?
Where?
When?
Why?
```

### 7. Architecture should match the source

A static historical dataset does not require a streaming architecture simply to appear more sophisticated.

---

# 23. Final Project State

After resolving the major blockers, the latest end-to-end pipeline run completed successfully.

Final database validation:

```text
customers: PASS
orders: PASS
products: PASS
sellers: PASS
category_translation: PASS
order_items: PASS
payments: PASS
reviews: PASS
```

Foreign-key validation:

```text
orders -> customers: PASS
order_items -> orders: PASS
order_items -> products: PASS
order_items -> sellers: PASS
payments -> orders: PASS
reviews -> orders: PASS
```

Final execution:

```text
Pipeline completed successfully in 69.48 seconds
```

The project therefore reached a repeatable, validated end-to-end ETL state after resolving the major development blockers.
