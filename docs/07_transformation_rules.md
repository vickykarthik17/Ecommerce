# Sprint 2: Data Transformation

Date: 13 August 2026

## Objective

Transform the validated raw Olist datasets into clean and analysis-ready datasets without changing the original files.

Raw data remains in:

`data/raw/`

Transformed data is stored in:

`data/processed/`

---

## 1. Transformation Approach

For each dataset, the process is:

1. Inspect the data
2. Identify required transformations
3. Standardize data types and values
4. Handle duplicates and nulls based on business meaning
5. Save the cleaned dataset
6. Validate the result

The raw data is never modified.

---

## 2. Customers Dataset

Source:

`olist_customers_dataset.csv`

Output:

`customers_clean.csv`

### Transformations

- Converted `customer_id` and `customer_unique_id` to string type because they are identifiers.
- Trimmed extra spaces from `customer_city`.
- Converted `customer_city` to lowercase for consistency.
- Converted `customer_state` to uppercase.
- Checked for duplicate and null customer IDs.

### Validation

- Rows: 99,441
- Columns: 5
- Duplicate `customer_id`: 0
- Null `customer_id`: 0
- Null `customer_unique_id`: 0

**Status: Complete**

---

## 3. Orders Dataset

Source:

`olist_orders_dataset.csv`

Output:

`orders_clean.csv`

### Transformations

- Converted `order_id` and `customer_id` to string type.
- Standardized `order_status` to lowercase.
- Converted all order date/time columns to Pandas datetime format.
- Preserved existing null values in delivery-related date columns because they may represent orders that were not completed or delivered.

### Date Columns

- `order_purchase_timestamp`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `order_estimated_delivery_date`

### Validation

- Rows: 99,441
- Columns: 8
- Duplicate `order_id`: 0
- Null `order_id`: 0
- Null `customer_id`: 0
- Date columns successfully converted to `datetime64[ns]`

Existing null values were preserved:

- `order_approved_at`: 160
- `order_delivered_carrier_date`: 1,783
- `order_delivered_customer_date`: 2,965

**Status: Complete**

---

## 4. Files Created

### Transformation scripts

- `src/transformation/inspect_data.py`
- `src/transformation/transform_customers.py`
- `src/transformation/validate_customers.py`
- `src/transformation/transform_orders.py`
- `src/transformation/validate_orders.py`

### Processed datasets

- `data/processed/customers_clean.csv`
- `data/processed/orders_clean.csv`

---

## 5. Sprint 2 Progress

### Completed on 13 August

- Transformation folder and processed-data folder created
- Transformation rules documented
- Customers dataset transformed and validated
- Orders dataset transformed and validated

### Remaining

The following datasets still need to be transformed:

1. Order Items
2. Payments
3. Reviews
4. Products
5. Sellers
6. Geolocation
7. Product Category Translation

---

## Current Status

**Sprint 2: In Progress**

**Completed:**
Customers → Transform → Validate  
Orders → Transform → Validate

**Next:**
Continue transformation of the remaining datasets.