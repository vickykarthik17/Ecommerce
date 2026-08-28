# Ecommerce ETL Project - Sprint-wise & Day-by-Day Development Log

> **Timeline:** August 10–24, 2026  
> **Scope:** End-to-end batch ETL pipeline using Python/Pandas and PostgreSQL.  
> **Purpose:** Preserve the meaningful development history, including implementation milestones, blockers, decisions, and finalization work.

## Sprint 1 - Source Profiling & Extraction
**August 10–12**

### August 10 - Project Initialization
- Created the Ecommerce ETL repository and initial project structure.
- Established the source-data foundation.
- Git initial commit created.

### August 11 - Source Profiling & Extraction Validation
- Inspected the nine Olist datasets.
- Set up the expected columns and basic source structure.
- Implemented extraction/source validation.
- Verified source row counts and column counts.
- Identified the raw geolocation dataset as the largest source, with 1,000,163 records.
- Git milestones: `Add ETL source profiling and extraction validation`, `Complete extraction validation`.

### August 12 - Extraction Refinement
- Refined extraction and validation logic.
- Began dataset-specific transformations.
- Added customer and order transformation logic.
- Kept each dataset's transformation in its own script so the logic stayed easier to follow.
- Git milestone: `Refine extraction and validation`.

---

## Sprint 2 - Transformation Layer
**August 13–16**

### August 13 - Customer & Order Transformations
- Implemented customer transformation.
- Implemented order transformation.
- Standardized and prepared processed outputs.
- Git milestone: `Add customer and order transformations`.

### August 14 - Transactional Transformations
- Completed transformations for customers, orders, order items, payments, and reviews.
- Added/updated validation for transformed datasets.
- Kept transformation logic modular by dataset.
- Git milestone: `Complete customer, order, item, payment, and review transformations`.

### August 15 - Remaining Transformations & Validation
- Completed transformations for products, sellers, geolocation, and category translation.
- Added validation scripts and overall processed-data validation.
- Removed duplicate geolocation records.
- Geolocation: 1,000,163 raw rows → 738,327 processed rows.
- Git milestone: `Completed Sprint 2 data transformations`.

### August 16 - Transformation Review & Documentation
- Reviewed the completed transformation layer.
- Updated Sprint 2 progress documentation.
- Reviewed the transformation results and validation output.
- Git milestone: `Update Sprint 2 progress documentation`.

---

## August 17 - Database Preparation
- Reviewed relationships between processed datasets.
- Prepared PostgreSQL table dependencies and loading requirements.
- Identified that foreign-key relationships would determine loading/reset order.

---

## Sprint 3 - PostgreSQL Loading & Database Validation
**August 18–20**

### August 18 - PostgreSQL Schema & Loading
- Created `sql/schema.sql`.
- Defined PostgreSQL tables and relational constraints.
- Added database configuration and loading scripts.
- Implemented bulk loading using PostgreSQL `COPY`.
- Added separate geolocation loading for the larger dataset.

#### Blockers resolved
**Product integer-format error**
- PostgreSQL rejected values such as `40.0` for integer columns.
- Investigation showed Pandas represented integer-like product fields as `float64`.
- Corrected the processed output before loading.

**Foreign-key truncate error**
- PostgreSQL rejected truncating a referenced parent table independently.
- Reset logic was changed to handle related tables in a dependency-aware manner.

- Git milestone: `Add PostgreSQL schema and loading pipeline`.

### August 19 - Database Validation & Repeat-safe Loading
- Completed PostgreSQL loading.
- Added `validate_database.py`.
- Added row-count validation.
- Added primary/composite-key validation.
- Added foreign-key validation.
- Made loading repeat-safe by resetting existing tables before the full refresh.
- Added end-to-end pipeline orchestration.
- Git milestones: `Complete PostgreSQL loading and validation`, `Add ETL pipeline orchestration and repeat-safe loading`.

### August 20 - End-to-End Stabilization
- Confirmed all nine processed datasets were included in the pipeline.
- Verified repeatable loading without duplicate-key failures.
- Verified extraction → transformation → loading → database validation as one workflow.
- Confirmed the project should remain a reusable **batch ETL pipeline**, rather than adding an artificial daily schedule to a static historical dataset.

---

## Sprint 4 - Orchestration, Logging & Error Handling
**August 21**

### August 21 - Logging & Error Handling
- Added `src/logging_config.py`.
- Added persistent logging to `logs/pipeline.log`.
- Added console and file logging.
- Added timestamps and step-level execution times.
- Added total pipeline execution timing.
- Added subprocess `stderr` capture.
- Added failure detection and immediate pipeline termination.

#### Failure test
- A real `transform_orders.py` failure occurred with:
  `OSError: [Errno 22] Invalid argument`.
- The orchestrator correctly captured the traceback, logged the failed step and timing, and stopped the pipeline.
- A subsequent run succeeded, confirming the pipeline and error-handling path.

#### Final check
- Full pipeline completed successfully in approximately 44.74 seconds on the development setup.
- Git milestone: `Add ETL logging and error handling`.

---

## Final Project Wrap-up Sprint
**August 22–24**

### August 22 - Documentation & Schema Refinement
- Refined the data dictionary.
- Updated transformation documentation.
- Corrected PostgreSQL schema definition where required.
- Finalized the project README.
- Git milestones:
  - `Refine data dictionary documentation`
  - `Update project documentation`
  - `Fix PostgreSQL schema definition`
  - `Finalize project README`

### August 23 - Repository Cleanup
- Cleaned `.gitignore`.
- Reviewed generated/runtime files and repository contents.
- Prepared the repository for final submission.
- Git milestone: `Clean up gitignore`.

### August 24 - Final Release / Submission Preparation
- Verify final branch state and working tree.
- Integrate the completed feature branch into the intended development/main flow.
- Run the complete pipeline from the final integration branch.
- Verify all nine database row counts.
- Verify key and foreign-key validation.
- Verify logging and failure handling.
- Remove temporary/debug/generated files.
- Check that credentials or secrets are not committed.
- Finalize README, data dictionary, transformation rules, architecture, setup, execution, validation, challenges, and limitations.
- Freeze the project after final verification.

---

# Major Challenges & Resolutions

## 1. Efficient database loading
**Problem:** Row-by-row inserts would create excessive database operations.

**Resolution:** PostgreSQL `COPY` was used for bulk loading.

## 2. Product values such as `40.0`
**Problem:** Pandas produced float-formatted values for integer-like product columns.

**Resolution:** Corrected the transformation/output representation before PostgreSQL loading.

## 3. Foreign-key constraints during reset
**Problem:** PostgreSQL prevented independent truncation of referenced tables.

**Resolution:** Reset related tables in a dependency-aware manner.

## 4. Duplicate-key errors on reruns
**Problem:** Reloading existing records caused primary-key conflicts.

**Resolution:** Added a repeat-safe full-refresh loading process.

## 5. Geolocation duplication
**Problem:** Raw geolocation contained 1,000,163 records with substantial duplication.

**Resolution:** Removed duplicates during transformation, producing 738,327 processed records.

## 6. Pipeline failures were difficult to trace
**Problem:** The orchestrator previously provided limited failure information.

**Resolution:** Added centralized logging and subprocess `stderr` capture.

## 7. Manual execution of many scripts
**Problem:** Each ETL stage previously had to be run separately.

**Resolution:** Added `run_pipeline.py` to execute the complete workflow sequentially and stop on failure.

---

# Final Pipeline

```text
Raw Olist CSVs
      ↓
Extraction
      ↓
Source Validation
      ↓
Transformation
      ↓
Data Quality Validation
      ↓
PostgreSQL Loading
      ↓
Database Validation
```

Supporting components:

```text
run_pipeline.py
 ├── orchestration
 ├── execution timing
 ├── error handling
 └── logging

logging_config.py
 ├── console logging
 └── persistent file logging

sql/schema.sql
 └── relational database structure
```

# Completion Checklist

- [x] Nine source datasets integrated
- [x] Extraction implemented
- [x] Source validation implemented
- [x] Dataset-specific transformations implemented
- [x] Transformation validation implemented
- [x] PostgreSQL schema implemented
- [x] Bulk loading implemented
- [x] Repeat-safe loading implemented
- [x] Database validation implemented
- [x] End-to-end orchestration implemented
- [x] Logging implemented
- [x] Error handling implemented
- [x] Failure behavior tested
- [x] README/documentation finalized
- [x] Repository cleanup started
- [ ] Final branch integration and submission freeze
