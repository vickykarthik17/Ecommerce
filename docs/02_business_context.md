# Business Context and Data Understanding

## 1. Purpose

Before transforming the Olist datasets, the business meaning of each dataset and the relationships between datasets were examined.

The objective was to understand what each table represents in an e-commerce system before deciding:

- Which columns should be transformed
- Which values should remain NULL
- Which fields are identifiers
- Which columns should be unique
- Which relationships should become foreign keys
- How the PostgreSQL schema should be designed

The transformation process therefore followed:

Business Meaning
        ↓
Data Structure
        ↓
Transformation Decision
        ↓
Validation
        ↓
Database Design

## 2. E-Commerce Business Model

The datasets represent different entities and events within an e-commerce system.

The major entities are:

- Customers
- Orders
- Products
- Sellers
- Order Items
- Payments
- Reviews
- Geolocation
- Product Category Translation

These datasets can be divided conceptually into:

### Master Data

- Customers
- Products
- Sellers
- Geolocation
- Category Translation

### Transactional Data

- Orders
- Order Items
- Payments
- Reviews

## 3. Customers

### Business Meaning

The customers dataset represents customers associated with the e-commerce orders.

Important fields include:

- customer_id
- customer_unique_id
- customer_zip_code_prefix
- customer_city
- customer_state

### Key Understanding

`customer_id` identifies the customer record referenced by the orders dataset.

The relationship is:

```text
customers
    ↓
orders
```

An individual customer can be associated with multiple orders.

### Transformation Considerations

Customer identifiers are treated as identifiers rather than numerical measurements.

Text fields are standardized where appropriate.

### Database Role

The customers table acts as a parent table for orders.

## 4. Orders

### Business Meaning

The orders dataset represents the order-level lifecycle of an e-commerce purchase.

Important fields include:

- order_id
- customer_id
- order_status
- order_purchase_timestamp
- order_approved_at
- order_delivered_carrier_date
- order_delivered_customer_date
- order_estimated_delivery_date

### Business Interpretation

The timestamp columns represent different stages in the lifecycle of an order.

Conceptually:

```text
Purchase
   ↓
Approval
   ↓
Carrier Handling
   ↓
Customer Delivery
```

The estimated delivery date represents the expected delivery rather than the actual delivery.

### Key Understanding

`order_id` identifies an order.

`customer_id` connects the order to the customer who placed it.

Therefore:

```text
customers.customer_id
          ↓
orders.customer_id
```

### Database Role

Orders is a central transactional table and acts as a parent for:

- Order Items
- Payments
- Reviews

## 5. Order Items

### Business Meaning

The order items dataset represents the individual products included within orders.

Important fields include:

- order_id
- order_item_id
- product_id
- seller_id
- shipping_limit_date
- price
- freight_value

### Key Understanding

One order can contain multiple items.

Therefore:

```text
Order
 ├── Item 1
 ├── Item 2
 └── Item 3
```

This means `order_id` alone cannot be treated as unique in the order items table.

The item-level record is identified using the appropriate combination of order and item identifiers.

### Relationships

```text
orders
    ↓
order_items
    ↓
products

order_items
    ↓
sellers
```

### Business Importance

This table connects the order transaction with the products and sellers involved in that transaction.

## 6. Products

### Business Meaning

The products dataset represents product-level information.

Important fields include:

- product_id
- product_category_name
- product_name_length
- product_description_length
- product_photos_qty
- product_weight_g
- product_length_cm
- product_height_cm
- product_width_cm

### Key Understanding

`product_id` is an identifier.

It should therefore be treated as a string rather than as a numerical measurement.

### Transformation Considerations

The source contained misspelled column names:

```text
product_name_lenght
product_description_lenght
```

These were standardized to:

```text
product_name_length
product_description_length
```

Numeric product attributes were also aligned with the PostgreSQL target datatypes.

### Relationship

```text
products.product_id
        ↑
order_items.product_id
```

## 7. Sellers

### Business Meaning

The sellers dataset represents sellers participating in the marketplace.

Important fields include:

- seller_id
- seller_zip_code_prefix
- seller_city
- seller_state

### Key Understanding

`seller_id` identifies a seller.

A seller can be associated with many order items.

Relationship:

```text
sellers
    ↓
order_items
```

### Database Role

The sellers table acts as a parent/master table for seller references in order items.

## 8. Payments

### Business Meaning

The payments dataset represents payment information associated with orders.

Important fields include:

- order_id
- payment_sequential
- payment_type
- payment_installments
- payment_value

### Key Understanding

An order can have multiple payment records.

Therefore, payment records should not automatically be reduced to one record per order.

The payment sequence helps distinguish multiple payment records associated with an order.

### Relationship

```text
orders
    ↓
payments
```

### Transformation Consideration

Payment values and installment counts need to retain their appropriate numeric meaning and datatype.

## 9. Reviews

### Business Meaning

The reviews dataset represents customer feedback associated with orders.

Important fields include:

- review_id
- order_id
- review_score
- review_comment_title
- review_comment_message
- review_creation_date
- review_answer_timestamp

### Key Understanding

Review text fields can legitimately contain missing values.

Therefore, NULL values were not automatically replaced simply to eliminate missing values.

### Relationship

```text
orders
    ↓
reviews
```

The review dataset is therefore connected to the order lifecycle.

## 10. Geolocation

### Business Meaning

The geolocation dataset contains geographical information associated with Brazilian ZIP-code prefixes.

Important fields include:

- geolocation_zip_code_prefix
- geolocation_lat
- geolocation_lng
- geolocation_city
- geolocation_state

### Data Volume

Raw records:

```text
1,000,163
```

Processed records:

```text
738,327
```

### Key Understanding

The raw dataset contains repeated geographical information.

Therefore, duplicate handling was performed during transformation.

### Database Role

Geolocation provides supporting geographical information that can be associated with customer and seller location information through ZIP-code prefixes.

## 11. Category Translation

### Business Meaning

The category translation dataset provides English translations for product category names.

Important fields include:

- product_category_name
- product_category_name_english

### Purpose

The dataset allows Portuguese product category names to be associated with their English equivalents.

Relationship conceptually:

```text
Product category
      ↓
Translation
      ↓
English category
```

### Data Volume

```text
71 records
```

This dataset is relatively small compared with the transactional datasets.

## 12. Relationship Between Major Tables

The core transactional relationships can be represented as:

```text
                 customers
                     │
                     │ customer_id
                     ↓
                  orders
                 /  |                   /   |                   ↓    ↓     ↓
      order_items payments reviews
          /            /             ↓       ↓
   products   sellers
```

Supporting datasets:

```text
products
    ↓
category_translation

customers ──→ geolocation
sellers   ──→ geolocation
```

The exact database constraints are validated separately during database validation.

## 13. Why Relationships Were Important

Understanding the relationships affected several engineering decisions.

### Primary Keys

Keys were selected based on the actual role of each table.

### Foreign Keys

Relationships were represented through foreign-key constraints where appropriate.

### Duplicate Validation

A field was not assumed to be unique simply because it contained an ID.

### Loading Order

Parent tables need to be available before dependent records can be loaded safely.

### Database Reset

Foreign-key relationships had to be considered when resetting tables before a full refresh.

## 14. Business Meaning and Transformation Decisions

The following principle was used throughout the project:

> A transformation should have a reason.

For example:

### Identifier

```text
product_id
```

Business meaning:

Product identifier.

Decision:

Treat as string.

Reason:

It identifies an entity rather than representing a quantity.

### Product Name Length

```text
product_name_length
```

Business meaning:

Length/count associated with the product name.

Decision:

Use an integer-compatible datatype.

Reason:

The field represents a count rather than a continuous measurement.

### Order Purchase Timestamp

```text
order_purchase_timestamp
```

Business meaning:

Time at which the order was placed.

Decision:

Preserve as a datetime field.

Reason:

It represents a meaningful event in the order lifecycle.

### Review Comment

```text
review_comment_message
```

Business meaning:

Customer-provided review text.

Decision:

Allow NULL.

Reason:

A missing review comment does not necessarily mean the review itself is invalid.

## 15. Data Cleaning Philosophy

The project did not follow a generic rule such as:

"Make every column non-null and remove every duplicate."

Instead, the approach was:

```text
What does this field mean?
        ↓
What is its expected structure?
        ↓
Is the current value actually invalid?
        ↓
What would changing it mean?
        ↓
What should the target database expect?
        ↓
Apply only the required transformation
        ↓
Validate
```

This prevents valid business information from being removed unnecessarily.

## 16. Business Understanding → Engineering Decisions

| Business Understanding | Engineering Decision |
|---|---|
| Customers can place multiple orders | Customer → Orders relationship |
| Orders can contain multiple products | Order items treated as detail records |
| Sellers can sell multiple items | Seller foreign-key relationship |
| Orders can have multiple payments | Payment records not forced to one per order |
| Review text may be absent | NULL values retained where appropriate |
| Product IDs identify products | IDs treated as strings |
| Product measurements/counts have numeric meaning | Appropriate numeric datatypes |
| Orders have lifecycle stages | Timestamp fields preserved |
| Geolocation contains repeated information | Duplicate handling applied |
| Dataset is static historical data | Full-refresh batch loading |

## 17. Summary

The business-context analysis established the structure required for the rest of the pipeline.

The process was:

```text
Understand business entities
        ↓
Understand relationships
        ↓
Profile source data
        ↓
Identify actual data issues
        ↓
Define targeted transformations
        ↓
Design relational schema
        ↓
Load data
        ↓
Validate integrity
```

The resulting pipeline is therefore based on the structure and meaning of the e-commerce data rather than on generic data-cleaning operations.
