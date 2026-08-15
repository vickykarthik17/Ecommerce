# Sprint 2: Data Transformation

Date: 15 August 2026

## Objective

Transform the validated raw Olist datasets into clean, consistent, and analysis-ready datasets for PostgreSQL loading.

The original files in `data/raw/` remain unchanged and are treated as the source of truth.

The transformed datasets are stored in:

`data/processed/`

---

## Transformation Approach

For each dataset:

1. Inspect the source data
2. Define the required transformation rules
3. Standardize data types and values
4. Handle duplicates and missing values according to business meaning
5. Validate the cleaned output
6. Save the processed dataset

This workflow was applied consistently across all tables so that the processed layer is reliable for downstream analysis and database ingestion.

Missing values were preserved when they represented valid business information, while duplicate and critical null checks were enforced where required for key integrity.

---

## 1. Customers

Output:

`customers_clean.csv`

### Transformations

- Converted customer identifiers to string.
- Trimmed and converted city names to lowercase.
- Converted state codes to uppercase.

### Validation

- Rows: 99,441
- Duplicate `customer_id`: 0
- Required identifier fields contain no nulls.

**Status: Complete**

---

## 2. Orders

Output:

`orders_clean.csv`

### Transformations

- Converted `order_id` and `customer_id` to string.
- Standardized `order_status` to lowercase.
- Converted order date columns to datetime.
- Preserved missing delivery and approval dates.

### Validation

- Rows: 99,441
- Duplicate `order_id`: 0
- Required identifier fields contain no nulls.

**Status: Complete**

---

## 3. Order Items

Output:

`order_items_clean.csv`

### Transformations

- Converted `order_id`, `product_id`, and `seller_id` to string.
- Kept `order_item_id` as an integer sequence.
- Converted `shipping_limit_date` to datetime.
- Kept price and freight values as numeric.

### Validation

- Rows: 112,650
- Duplicate `order_id + order_item_id`: 0
- No null values.

**Status: Complete**

---

## 4. Payments

Output:

`payments_clean.csv`

### Transformations

- Converted `order_id` to string.
- Standardized `payment_type` to lowercase.
- Kept payment sequence, installments, and value as numeric fields.

### Validation

- Rows: 103,886
- Duplicate `order_id + payment_sequential`: 0
- No null values.

**Status: Complete**

---

## 5. Reviews

Output:

`reviews_clean.csv`

### Transformations

- Converted `review_id` and `order_id` to string.
- Converted review date fields to datetime.
- Kept `review_score` as an integer.
- Preserved missing review comments because they are optional.

### Validation

- Rows: 99,224
- Duplicate `review_id + order_id`: 0
- Required fields contain no nulls.

**Status: Complete**

---

## 6. Products

Output:

`products_clean.csv`

### Transformations

- Converted `product_id` to string.
- Standardized product category names to lowercase.
- Corrected source column naming:
  - `product_name_lenght` → `product_name_length`
  - `product_description_lenght` → `product_description_length`
- Preserved missing product attributes.

### Validation

- Rows: 32,951
- Duplicate `product_id`: 0

**Status: Complete**

---

## 7. Sellers

Output:

`sellers_clean.csv`

### Transformations

- Converted `seller_id` to string.
- Standardized city names to lowercase.
- Standardized state codes to uppercase.
- Kept ZIP code prefix as numeric.

### Validation

- Rows: 3,095
- Duplicate `seller_id`: 0
- No null values.

**Status: Complete**

---

## 8. Geolocation

Output:

`geolocation_clean.csv`

### Transformations

- Standardized city names to lowercase.
- Standardized state codes to uppercase.
- Removed exact duplicate rows.
- Repeated ZIP code prefixes were preserved because they can represent multiple valid geographic records.

### Validation

- Original rows: 1,000,163
- Exact duplicates removed: 261,836
- Final rows: 738,327
- Duplicate rows after transformation: 0
- No null values.

**Status: Complete**

---

## 9. Product Category Translation

Output:

`category_translation_clean.csv`

### Transformations

- Standardized both category fields to lowercase.
- Trimmed extra spaces.

### Validation

- Rows: 71
- Duplicate `product_category_name`: 0
- No null values.

**Status: Complete**

---

## Overall Sprint 2 Validation

All 9 datasets were transformed and validated as part of the Sprint 2 data preparation workflow.

The final processed layer was reviewed for:

- Expected file creation
- Row and column counts
- Primary and composite key uniqueness
- Null values and missing-data handling
- Duplicate record removal or preservation based on business meaning
- Data-type standardization for identifiers, dates, and numeric fields

Across the cleaned datasets, the processed layer reflects a consistent and reliable foundation for PostgreSQL ingestion and downstream business analysis.

---

## Sprint 2 Status

**Completed:**

- Data transformation across all 9 Olist datasets
- Data quality validation for key fields and duplicate checks
- Processed dataset creation in `data/processed/`
- Transformation documentation and summary reporting

**Current outcome:**

The transformation stage is complete and the processed datasets are ready for the next step: loading into PostgreSQL.

---

## Final Sprint 2 Summary

The transformation work followed a consistent approach for all datasets: standardize names, normalize IDs, convert date columns to datetime, preserve valid nulls, remove meaningful duplicates, and confirm key integrity before saving. This ensures the processed layer is not only clean but also logically aligned with the source data and business requirements.

Throughout the sprint, every dataset was validated individually, and the combined processed layer was checked at an overall level. The resulting structure is coherent, internally consistent, and ready for database loading and analytical use.

**Overall result: Successful completion of Sprint 2 data transformation and validation.**
3. Generate comprehensive data quality report
4. Archive raw data backups and document transformation lineage