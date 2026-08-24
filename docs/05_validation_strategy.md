# Validation Strategy

## 1. Purpose

Validation is used throughout the ETL pipeline to detect structural, data-quality, and database-integrity problems before they can affect downstream processing.

Validation is not performed only after loading into PostgreSQL.

The pipeline uses multiple validation stages:

```text
Raw CSV
   ↓
Source Validation
   ↓
Transformation
   ↓
Processed Data Validation
   ↓
PostgreSQL Loading
   ↓
Database Validation
```

This creates quality gates at each major stage.

---

## 2. Why Multiple Validation Stages Are Used

A failure at different stages can have different causes.

For example:

- A missing source column is an extraction/source problem.
- An unexpected NULL may be a transformation/data-quality issue.
- A datatype mismatch may become visible during database loading.
- A missing foreign-key reference is a relational-integrity problem.

Therefore, one final validation step is not sufficient.

The strategy is:

```text
Validate early
      ↓
Transform safely
      ↓
Validate again
      ↓
Load
      ↓
Validate database integrity
```

---

# 3. Source Validation

The first validation stage operates on the raw source files.

Relevant files:

```text
src/extraction/expected_columns.py
src/extraction/validate_data.py
```

## Purpose

Source validation ensures that the pipeline is working with the expected input structure.

It checks whether:

- Expected source files exist
- Expected columns are present
- The source structure matches the expected definitions

The extraction stage also reports:

- Number of rows
- Number of columns
- Validation status

---

## 4. Source Dataset Validation Results

The extraction stage successfully validated all nine source datasets.

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

This confirms that the expected input structure was available before transformations began.

---

# 5. Transformation-Level Validation

After all transformations are completed, the pipeline runs:

```text
src/transformation/validate_all.py
```

The purpose is to validate the processed CSV files before they are loaded into PostgreSQL.

The validation checks include:

- Row count
- Column count
- NULL values
- Duplicate-key conditions

---

# 6. Row Count Validation

Row counts provide a basic reconciliation check.

The transformed row count is compared with the expected result for each processed dataset.

Latest validation results:

| Dataset | Rows |
|---|---:|
| customers_clean.csv | 99,441 |
| orders_clean.csv | 99,441 |
| order_items_clean.csv | 112,650 |
| payments_clean.csv | 103,886 |
| reviews_clean.csv | 99,224 |
| products_clean.csv | 32,951 |
| sellers_clean.csv | 3,095 |
| geolocation_clean.csv | 738,327 |
| category_translation_clean.csv | 71 |

Row counts are especially useful for detecting unexpected data loss during transformations.

---

# 7. Column Count Validation

The validation stage also checks the number of columns in each processed dataset.

Latest results:

| Dataset | Columns |
|---|---:|
| customers_clean.csv | 5 |
| orders_clean.csv | 8 |
| order_items_clean.csv | 7 |
| payments_clean.csv | 5 |
| reviews_clean.csv | 7 |
| products_clean.csv | 9 |
| sellers_clean.csv | 4 |
| geolocation_clean.csv | 5 |
| category_translation_clean.csv | 2 |

This helps detect accidental column removal or unexpected schema changes during transformation.

---

# 8. NULL Validation

NULL counts are reported for every processed dataset.

Latest results:

| Dataset | NULL values |
|---|---:|
| customers_clean.csv | 0 |
| orders_clean.csv | 4,908 |
| order_items_clean.csv | 0 |
| payments_clean.csv | 0 |
| reviews_clean.csv | 145,903 |
| products_clean.csv | 2,448 |
| sellers_clean.csv | 0 |
| geolocation_clean.csv | 0 |
| category_translation_clean.csv | 0 |

## Important Interpretation

A non-zero NULL count is not automatically considered a validation failure.

For example:

```text
orders_clean.csv
NULL values: 4,908
```

Some order lifecycle timestamps can legitimately be missing.

Similarly:

```text
reviews_clean.csv
NULL values: 145,903
```

can include missing optional review text.

The validation stage reports NULLs so they can be evaluated according to business meaning.

---

# 9. Duplicate-Key Validation

Duplicate-key validation checks whether fields expected to identify individual records contain unexpected duplicates.

Latest results:

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

## Important Business Rule

Duplicate validation is based on the role of the dataset.

For example, `order_id` cannot simply be declared unique in `order_items` because one order can contain multiple items.

Therefore, validation rules must reflect the actual business structure.

---

# 10. Database Validation

After all processed datasets are loaded into PostgreSQL, the pipeline runs:

```text
src/loading/validate_database.py
```

This is the final validation layer.

It checks:

1. Row counts
2. Key validity
3. Foreign-key relationships

---

# 11. Database Row-Count Validation

The latest successful pipeline execution produced:

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

These counts match the processed datasets loaded by the pipeline.

This provides a basic reconciliation between the processed files and the PostgreSQL database.

---

# 12. Primary/Key Validation

The database validation stage reported:

```text
--- KEY VALIDATION ---

customers: PASS
orders: PASS
products: PASS
sellers: PASS
category_translation: PASS
order_items: PASS
payments: PASS
reviews: PASS
```

This confirms that the implemented key validation checks passed for all listed tables.

---

# 13. Foreign-Key Validation

The implemented relationships were validated as follows:

```text
orders -> customers: PASS

order_items -> orders: PASS
order_items -> products: PASS
order_items -> sellers: PASS

payments -> orders: PASS

reviews -> orders: PASS
```

These checks confirm that the referenced parent records exist for the relationships tested by the validation process.

---

# 14. Referential Integrity Model

The foreign-key validation can be represented as:

```text
customers
    │
    │ customer_id
    ↓
orders
 ┌──┼──────────────┐
 │  │              │
 ↓  ↓              ↓
items payments   reviews
 │
 ├──────────→ products
 │
 └──────────→ sellers
```

The validation process ensures that dependent records do not reference missing parent records in the implemented relationships.

---

# 15. Why Foreign-Key Validation Matters

A dataset can pass row-count validation while still containing invalid relationships.

For example:

```text
orders
customer_id = ABC
```

If customer `ABC` does not exist in the customers table, the row count alone would not identify the problem.

Foreign-key validation detects this type of integrity issue.

Therefore:

```text
Row Count Validation
        +
Key Validation
        +
Foreign-Key Validation
```

provides stronger confidence in the loaded relational data.

---

# 16. Validation After Transformation vs Validation After Loading

These two validation stages serve different purposes.

### Transformation Validation

Answers:

> Are the processed CSV files structurally and qualitatively acceptable?

It checks:

- Rows
- Columns
- NULLs
- Duplicate-key conditions

### Database Validation

Answers:

> Did the processed datasets load correctly into PostgreSQL and preserve the required relational integrity?

It checks:

- Database row counts
- Keys
- Foreign-key relationships

Therefore:

```text
Processed Data Validation
        ↓
Data is ready to load

Database Validation
        ↓
Loaded relational data is structurally valid
```

---

# 17. Validation as a Quality Gate

Each major stage acts as a quality gate.

```text
                    QUALITY GATES

Raw Data
   │
   ▼
Source Validation
   │
   │ PASS
   ▼
Transformation
   │
   ▼
Processed Data Validation
   │
   │ PASS
   ▼
PostgreSQL Loading
   │
   ▼
Database Validation
   │
   │ PASS
   ▼
Pipeline Complete
```

If a critical stage fails, the pipeline should not continue blindly.

---

# 18. Validation and Error Handling

Validation and error handling work together.

For example, during development the pipeline encountered a PostgreSQL duplicate-key error:

```text
duplicate key value violates unique constraint "customers_pkey"
```

The problem was traced to rerunning the pipeline without resetting the existing database records.

The loading strategy was then changed to support a controlled full refresh.

This demonstrates the relationship between:

```text
Validation
    ↓
Detect problem
    ↓
Investigate cause
    ↓
Change implementation
    ↓
Rerun
    ↓
Validate again
```

---

# 19. Validation and Datatype Compatibility

The product datatype issue also demonstrated why validation cannot be limited to simple row counts.

A product field contained values such as:

```text
40.0
```

while PostgreSQL expected an integer-compatible datatype.

The database rejected the data.

The transformation was then updated to align the value with the target schema.

After the change, the complete pipeline loaded successfully.

This shows that:

```text
Source validation
        ↓
Transformation validation
        ↓
Database validation
```

are complementary rather than interchangeable.

---

# 20. Validation Philosophy

The validation strategy does not attempt to prove that the dataset is perfect.

Instead, it verifies the conditions that matter for the implemented pipeline.

The approach is:

```text
Define expected condition
        ↓
Check condition
        ↓
Report result
        ↓
Investigate failures
        ↓
Fix root cause
        ↓
Validate again
```

This makes validation explicit and repeatable.

---

# 21. What the Current Validation Does Not Guarantee

The implemented validation does not guarantee every possible form of data quality.

For example, it does not automatically prove:

- Business correctness of every individual value
- Accuracy of external source information
- Absence of every possible anomaly
- Correctness of every analytical interpretation
- Absence of all NULL values

Instead, it validates the structural, key, and relational conditions implemented for this ETL project.

Additional business-specific checks can be added if the project requirements expand.

---

# 22. Final Validation Result

The latest end-to-end execution completed successfully.

The final output reported:

```text
Database validation completed.
Pipeline completed successfully in 69.48 seconds
```

Database row counts were successfully produced for all nine target tables.

All implemented key validations passed.

All implemented foreign-key validations passed.

Therefore, the current ETL pipeline successfully passes its implemented source, transformation, and database validation stages.

---

# 23. Validation Summary

The complete validation strategy is:

```text
SOURCE
│
├── Expected files
├── Expected columns
├── Row count
└── Source structure
        │
        ▼
TRANSFORMATION
│
├── Row count
├── Column count
├── NULL reporting
└── Duplicate-key checks
        │
        ▼
DATABASE
│
├── Row counts
├── Key validation
└── Foreign-key validation
        │
        ▼
PIPELINE COMPLETE
```

The validation layer therefore acts as a set of controlled quality gates between extraction, transformation, and loading.
