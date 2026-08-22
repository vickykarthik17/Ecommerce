\# 08: PostgreSQL Schema



\## 1. Purpose



PostgreSQL is used as the target database for the transformed Olist datasets.



The schema organizes the datasets into related tables using primary keys, composite keys, and foreign keys.



\---



\## 2. Database



\*\*Database:\*\* `ecommerce`  

\*\*PostgreSQL Version:\*\* 18



The database contains nine tables:



```text

customers

orders

order\_items

payments

reviews

products

sellers

geolocation

category\_translation



3\. Table Design

Customers



Table: customers



Primary Key:



customer\_id



Stores customer-level information such as:



Customer identifier

Customer unique identifier

ZIP code prefix

City

State

Orders



Table: orders



Primary Key:



order\_id



Foreign Key:



customer\_id → customers.customer\_id



Stores order-level information including:



Order status

Purchase timestamp

Approval timestamp

Carrier delivery date

Customer delivery date

Estimated delivery date

Order Items



Table: order\_items



Composite Primary Key:



order\_id + order\_item\_id



Foreign Keys:



order\_id   → orders.order\_id

product\_id → products.product\_id

seller\_id  → sellers.seller\_id



Stores individual products and sellers associated with each order.



Products



Table: products



Primary Key:



product\_id



Stores product information such as:



Product category

Product name length

Product description length

Number of photos

Weight

Dimensions

Sellers



Table: sellers



Primary Key:



seller\_id



Stores seller identifiers and location information.



Payments



Table: payments



Composite Primary Key:



order\_id + payment\_sequential



Foreign Key:



order\_id → orders.order\_id



Stores payment method, installments, and payment value for each order.



Reviews



Table: reviews



Composite Primary Key:



review\_id + order\_id



Foreign Key:



order\_id → orders.order\_id



Stores review scores, comments, and review timestamps.



The composite key is used because review\_id alone was not unique in the source data.



Geolocation



Table: geolocation



Primary Key:



geolocation\_id



The primary key is a PostgreSQL-generated identity column.



The ZIP code prefix is not used as the primary key because multiple geolocation records can share the same ZIP prefix.



Category Translation



Table: category\_translation



Primary Key:



product\_category\_name



Stores the English translation of product category names.



4\. Relationship Structure



The main relationships are:



customers

&#x20;   :

&#x20;   └── orders

&#x20;         :

&#x20;         ├── order\_items ── products

&#x20;         :        :

&#x20;         :        └── sellers

&#x20;         :

&#x20;         ├── payments

&#x20;         :

&#x20;         └── reviews



Additional reference data:



products

&#x20;   :

&#x20;   └── category\_translation



Geolocation is stored separately because ZIP code prefixes are not unique.



5\. Key Design Decisions

Customer Key

customer\_id



is the primary key for the customers table.



customer\_unique\_id is retained as a business identifier but is not used as the primary key.



Order Item Key

order\_id + order\_item\_id



uniquely identifies an item within an order.



Payment Key

order\_id + payment\_sequential



allows multiple payment records for the same order.



Review Key

review\_id + order\_id



is used because individual review IDs were repeated in the source data.



Geolocation Key



A generated geolocation\_id is used because ZIP prefixes can have multiple valid geographic records.



6\. Referential Integrity



Foreign keys enforce relationships between the main transactional tables.



The implemented relationships are:



orders.customer\_id

&#x20;   → customers.customer\_id



order\_items.order\_id

&#x20;   → orders.order\_id



order\_items.product\_id

&#x20;   → products.product\_id



order\_items.seller\_id

&#x20;   → sellers.seller\_id



payments.order\_id

&#x20;   → orders.order\_id



reviews.order\_id

&#x20;   → orders.order\_id

7\. Database Validation



After loading the transformed datasets, the database validation script checks:



Row counts

Duplicate primary/composite keys

Foreign-key relationships



The final validation completed successfully.



Key Validation       : PASS

Foreign Key Validation: PASS

8\. Loading Strategy



The transformed CSV files are loaded using PostgreSQL COPY.



The pipeline uses a full-refresh approach:



TRUNCATE existing tables

&#x20;       :

&#x20;       ↓

Load processed CSV files

&#x20;       :

&#x20;       ↓

Validate database



This approach is suitable for the static Olist historical dataset and makes repeated pipeline execution deterministic.



9\. Result



The PostgreSQL database provides a structured relational target for the transformed Olist data while enforcing the important relationships and uniqueness rules identified during the ETL process.





\*\*Before committing this file\*\*, we should fix and verify the `schema.sql` comma issue. Don't edit it yet.



Run:



```powershell

python src/loading/validate\_database.py





