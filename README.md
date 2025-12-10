# Financial-ETL-pipeline-and-dashboard
Customer transaction analytics &amp; risk insights


## 1) Project summary / problem statement (elevator pitch)

### Project title: Customer transaction analytics & risk insights — end-to-end ETL, analytics, and interactive Tableau Public dashboards.

### Problem statement: Banks and fintechs must monitor customer transactions to maximize lifetime value and minimize risk. This project uses transaction-level data to answer business questions such as:

• Who are our most valuable customers (by deposits & fees)?

• Where do fraud losses and risk concentrations exist?

• Which customer segments are likely to churn?

• Which merchant categories and channels drive revenue/growth or risk?

### Outcome/business value:

A single analytics pipeline and interactive dashboards that let product, risk, and finance teams explore revenue, transaction trends, risk (fraud), and customer health, enabling targeted retention campaigns, fraud mitigation, and more profitable product prioritization.


### Tools & Technology Stack
*   Jupyter Notebook: Used for initial data exploration, analysis, and prototyping.
*   Prefect: Orchestrates the ETL pipeline, ensuring reliable and repeatable data workflows.
*   dbt Core (with MySQL): Performs data transformations, cleaning, and modeling within the MySQL data warehouse.
*   MySQL: Serves as the primary data warehouse, storing both raw and transformed data.
*   Tableau Public: Creates interactive dashboards and visualizations for data exploration and presentation.

  ## 📂 Project Dataset

You can **click below to view or download the financial transactions dataset** used in this project:

[ Download/View Financial Transactions Dataset](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/financial_transactions_2000.csv)

> **Note:** This is a synthetic dataset generated for demonstration purposes. It simulates realistic financial transactions, customers, and fraud patterns.


## ETL & analysis workflow

### Ingest (Extract)

* Source: local CSV (for this project) — later could be S3, API, or streaming.

* Tools: Python + pandas or an ingestion job using Airflow operator (S3ToGCS / S3ToRedshift etc.)

* Validate schema (types, nulls), sampling quality checks, row counts.


#### Stage & raw layer

* Load raw CSV into a raw.transactions table in my data warehouse (keep exactly as ingested).

* Keep raw files/metadata (source filename, ingestion timestamp, row_count).


## Transform (Cleaning + business logic)


* Remove duplicates based on transaction_id.

  ![Remove duplicates screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Remove%20duplicates%20screenshot%2010.JPG?raw=true)


* Normalize merchant categories (mapping table).


![Apply Normalization Screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Apply%20normalization.JPG?raw=true)


* Convert transaction_date to date/time with timezone if needed.

* Add flags: is_recurring (if merchant repeated each month), is_salary, rolling_30d_spend, active_30d etc.


### Aggregate base tables:

* dim_customers — 1 row per customer (customer-level attributes)

* fact_transactions — cleaned transactions

* agg_customer_monthly — monthly aggregates per customer


## Enrich

* Join external tables (merchant risk score, MCC codes, macro indicators).

* Feature engineering for churn/fraud:

* tx_count_30d, avg_amount_90d, pct_online_tx, decline_rate, largest_tx_amount, gini_spend (concentration)

* label churn = no tx in last X months (choose X = 3/6)

## Load to the analytics layer

* Store final models/tables: mart_customer_health, mart_fraud_alerts, mart_revenue_by_category.


### Orchestration & Scheduling

* Use Airflow: schedule daily ingestion, dbt models run after load, tests.

* Track DAG run statuses & SLAs.

### Monitoring & data quality
* Row-count checks, null rate thresholds, value distribution drift detection.
