# Data Profiling

## 1. Purpose

Data profiling was performed before applying transformations so that cleaning decisions were based on observed data characteristics rather than arbitrary rules.

The profiling process focused on:

- Row counts
- Column counts
- Expected columns
- Missing values
- Duplicate records
- Data types
- Dataset size
- Structural consistency
- Potential datatype mismatches
- Relationships relevant to database loading

The overall approach was:

```text
Raw Data
   ↓
Inspect Structure
   ↓
Validate Expected Columns
   ↓
Profile Data Quality
   ↓
Identify Actual Issues
   ↓
Define Transformations
```

---

## 2. Source Datasets

The source consists of nine CSV datasets.

| Dataset | Rows | Columns | Purpose |
|---|---:|---:|---|
| olist_customers_dataset.csv | 99,441 | 5 | Customer information |
| olist_geolocation_dataset.csv | 1,000,163 | 5 | Geographical information |
| olist_order_items_dataset.csv | 112,650 | 7 | Products included in orders |
| olist_order_payments_dataset.csv | 103,886 | 5 | Payment records |
| olist_order_reviews_dataset.csv | 99,224 | 7 | Customer reviews |
| olist_orders_dataset.csv | 99,441 | 8 | Order lifecycle information |
| olist_products_dataset.csv | 32,951 | 9 | Product information |
| olist_sellers_dataset.csv | 3,095 | 4 | Seller information |
| product_category_name_translation.csv | 71 | 2 | Product category translations |

These counts were confirmed during the extraction stage.

---

## 3. Source Structure Validation

Before transformation, the extraction process validates that the expected source files exist and that their columns match the expected structure.

The extraction stage reported all nine source datasets as:

```text
Valid
```

This established that the pipeline was operating on the expected source structure before transformation began.

The expected column definitions are maintained separately in:

```text
src/extraction/expected_columns.py
```

This prevents the transformation layer from silently processing an unexpected file structure.

---

## 4. Customers Profiling

### Observed Structure

```text
Rows: 99,441
Columns: 5
```

The customer dataset contains customer identifiers and location information.

### Key Observations

- `customer_id` is used as the customer record identifier.
- Customer location fields are text attributes.
- Customer records participate in the relationship with orders.

### Transformation Implication

Customer identifiers should remain identifier fields rather than being treated as numerical values.

---

## 5. Orders Profiling

### Observed Structure

```text
Rows: 99,441
Columns: 8
```

The orders dataset contains order identifiers, customer references, status information, and lifecycle timestamps.

### Key Observations

Several timestamp fields represent different stages of the order lifecycle.

Some fields contain missing values.

After transformation validation:

```text
Rows: 99,441
Columns: 8
Null values: 4,908
Duplicate key: 0
```

### Interpretation

The presence of NULL values was not automatically treated as a data-quality failure.

Some order lifecycle timestamps can legitimately be unavailable depending on the state of an order.

### Transformation Implication

Datetime fields were treated according to their business meaning rather than replacing missing values arbitrarily.

---

## 6. Order Items Profiling

### Observed Structure

```text
Rows: 112,650
Columns: 7
```

The dataset represents individual products included in orders.

### Key Observation

An order can contain multiple items.

Therefore:

```text
order_id
```

cannot be treated as a unique key within the order-items dataset.

### Transformation Validation

```text
Rows: 112,650
Columns: 7
Null values: 0
Duplicate key: 0
```

### Transformation Implication

The order-item structure was preserved rather than collapsing multiple items into one order-level record.

---

## 7. Payments Profiling

### Observed Structure

```text
Rows: 103,886
Columns: 5
```

### Key Observation

An order can have multiple payment records.

The payment sequence provides information for distinguishing multiple payment records associated with an order.

### Transformation Validation

```text
Rows: 103,886
Columns: 5
Null values: 0
Duplicate key: 0
```

### Transformation Implication

Payment records were retained at their original transactional level.

---

## 8. Reviews Profiling

### Observed Structure

```text
Rows: 99,224
Columns: 7
```

### Key Observation

Review text fields can contain missing values.

After transformation validation:

```text
Rows: 99,224
Columns: 7
Null values: 145,903
Duplicate key: 0
```

### Interpretation

The NULL count represents missing values across columns, not necessarily invalid review records.

A missing review comment does not mean that the entire review is invalid.

### Transformation Implication

Missing review information was not blindly replaced with arbitrary values.

---

## 9. Products Profiling

### Observed Structure

```text
Rows: 32,951
Columns: 9
```

### Key Observations

The products dataset contains:

- Product identifiers
- Category information
- Product name length
- Description length
- Photo count
- Weight
- Dimensions

A datatype mismatch was discovered during PostgreSQL loading.

Values such as:

```text
40.0
44.0
46.0
```

were being interpreted by Pandas as floating-point values while the PostgreSQL target expected an integer-compatible datatype.

### Resolution

The relevant fields were explicitly converted to appropriate integer-compatible values during transformation.

### Transformation Validation

```text
Rows: 32,951
Columns: 9
Null values: 2,448
Duplicate key: 0
```

### Transformation Implication

Source datatype inference was not assumed to match the target PostgreSQL schema.

---

## 10. Sellers Profiling

### Observed Structure

```text
Rows: 3,095
Columns: 4
```

Seller records contain seller identifiers and location attributes.

### Transformation Validation

```text
Rows: 3,095
Columns: 4
Null values: 0
Duplicate key: 0
```

### Transformation Implication

`seller_id` was treated as an identifier and used as the parent reference for seller information in order items.

---

## 11. Geolocation Profiling

### Observed Structure

```text
Raw rows: 1,000,163
Columns: 5
```

This was the largest source dataset.

### Key Observation

The raw geolocation dataset contained repeated geographical records.

The transformation removed duplicate records.

### Processed Result

```text
Rows: 738,327
Columns: 5
Null values: 0
```

This represents a reduction of:

```text
1,000,163 - 738,327 = 261,836 rows
```

The reduction was therefore based on duplicate handling rather than arbitrary row removal.

### Transformation Implication

Because geolocation is supporting geographical data, duplicate geographical records did not provide additional business information for the processed dataset.

---

## 12. Category Translation Profiling

### Observed Structure

```text
Rows: 71
Columns: 2
```

The dataset maps product category names to English translations.

### Transformation Validation

```text
Rows: 71
Columns: 2
Null values: 0
Duplicate key: 0
```

### Transformation Implication

The small reference dataset was retained as a separate lookup table rather than merging it permanently into the products dataset.

---

## 13. Processed Data Validation Summary

After transformation, the validation stage produced:

| Dataset | Rows | Columns | Null Values | Duplicate Key |
|---|---:|---:|---:|---:|
| customers_clean.csv | 99,441 | 5 | 0 | 0 |
| orders_clean.csv | 99,441 | 8 | 4,908 | 0 |
| order_items_clean.csv | 112,650 | 7 | 0 | 0 |
| payments_clean.csv | 103,886 | 5 | 0 | 0 |
| reviews_clean.csv | 99,224 | 7 | 145,903 | 0 |
| products_clean.csv | 32,951 | 9 | 2,448 | 0 |
| sellers_clean.csv | 3,095 | 4 | 0 | 0 |
| geolocation_clean.csv | 738,327 | 5 | 0 | — |
| category_translation_clean.csv | 71 | 2 | 0 | 0 |

The validation results were used before database loading.

---

## 14. NULL Analysis

NULL values were evaluated according to the meaning of the relevant field.

The project did not use a blanket rule such as:

```text
Replace every NULL with 0
```

or:

```text
Delete every row containing NULL
```

Instead, the question was:

> Does the missing value represent an invalid record, or does it represent legitimate missing business information?

Examples include:

- Missing order lifecycle timestamps
- Missing review comments
- Missing optional product attributes

Where no reliable business rule existed for replacement, NULL was retained.

---

## 15. Duplicate Analysis

Duplicate handling was also dataset-specific.

The project did not remove duplicates indiscriminately.

For geolocation, repeated geographical records were identified as redundant and removed during transformation.

For transactional datasets, repeated entity references were not automatically treated as duplicates.

For example:

```text
order_id = X
order_item_id = 1
order_item_id = 2
```

represents two legitimate order-item records rather than a duplicate order.

---

## 16. Datatype Analysis

Datatype profiling was important because the source files are CSV files and therefore do not enforce a database schema.

The pipeline had to align:

```text
Source CSV
    ↓
Pandas datatype
    ↓
Transformed datatype
    ↓
PostgreSQL datatype
```

The product datatype issue demonstrated why this validation is necessary.

A value such as:

```text
40.0
```

may be numerically equivalent to:

```text
40
```

but PostgreSQL still distinguishes between numeric datatypes when loading data into a typed column.

---

## 17. Profiling → Transformation Decisions

| Profiling Observation | Transformation Decision |
|---|---|
| Source files matched expected structure | Proceed with extraction |
| Customer IDs represent entities | Preserve as identifiers |
| Order timestamps contain lifecycle information | Preserve datetime meaning |
| Orders can contain multiple items | Preserve item-level records |
| Orders can have multiple payments | Preserve payment-level records |
| Review text can be missing | Retain appropriate NULL values |
| Product numeric fields had datatype mismatch | Convert to target-compatible types |
| Geolocation contained repeated records | Remove redundant duplicates |
| Category translation is a reference dataset | Keep as separate lookup table |
| Static historical source dataset | Use full-refresh database loading |

---

## 18. Profiling Philosophy

The profiling stage was not intended merely to produce statistics.

Its purpose was to answer engineering questions:

1. What does the dataset contain?
2. What does each field mean?
3. Which values are actually problematic?
4. Which values are legitimately missing?
5. Which fields are identifiers?
6. Which relationships exist between datasets?
7. What does PostgreSQL expect?
8. What transformation is necessary?
9. How can the transformation be validated?

This ensured that the ETL process was based on evidence from the data.

---

## 19. Overall Profiling Workflow

```text
Extract source datasets
        ↓
Check expected files
        ↓
Validate expected columns
        ↓
Inspect row/column counts
        ↓
Inspect missing values
        ↓
Inspect duplicates
        ↓
Inspect datatypes
        ↓
Understand business meaning
        ↓
Identify actual issues
        ↓
Define transformations
        ↓
Validate transformed datasets
        ↓
Load into PostgreSQL
```

---

## 20. Final Profiling Outcome

The profiling stage established that:

- All nine expected source datasets were present.
- All expected source structures were valid.
- The datasets have different business roles and relationship patterns.
- NULL values exist in several datasets and are not automatically invalid.
- Geolocation is significantly larger than the other datasets.
- Geolocation contains redundant records that can be removed safely.
- Product datatype compatibility required explicit handling.
- Transactional datasets must preserve their one-to-many relationships.
- The final transformed datasets passed the implemented validation checks.

The profiling findings directly informed the transformation logic, PostgreSQL schema, loading strategy, and validation rules.
