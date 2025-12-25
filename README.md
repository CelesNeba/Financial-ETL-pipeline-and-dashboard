# Automated Financial-ETL-pipeline-and-dashboard
Customer transaction analytics & risk insights


## 1) Project summary/problem statement (elevator pitch)

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


Insert Values Into Merchant Category

![Insert Values Into Merchant Category Screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Insert%20values%20into%20mercharnt%20category%20screenshot.JPG?raw=true)



Apply normalization 

![Apply Normalization Screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Apply%20normalization.JPG?raw=true)


* Convert transaction_date to date/time with timezone if needed.


![Convert transaction_date to proper DATETIME](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Convert%20transaction_date%20to%20proper%20DATETIME.JPG?raw=true)


* Add flags: is_recurring (if merchant repeated each month), is_salary, rolling_30d_spend, active_30d etc.


![Behavioural flag screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Behavioural%20flag%20screenshot.JPG?raw=true)


![is_salary flag](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/is_salary%20flag.JPG?raw=true)


![is_recurring (merchant used every month)](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/is_recurring%20(merchant%20used%20every%20month).JPG?raw=true)


![rolling_30d_spend (window sum) screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/rolling_30d_spend%20(window%20sum)%20screenshot.JPG?raw=true)



![active_30d (customer made any transaction in last 30 days) screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/active_30d%20(customer%20made%20any%20transaction%20in%20last%2030%20days)%20screenshot.JPG?raw=true)







### Aggregate base tables:

* dim_customers — 1 row per customer (customer-level attributes)


![dim_customers table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/dim_customers%20table.JPG?raw=true)


* fact_transactions — cleaned transactions

![fact_transactions Table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/fact_transactions%20Table.JPG?raw=true)



* agg_customer_monthly — monthly aggregates per customer


![Agg customers monthly table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Agg%20customers%20monthly%20table.JPG?raw=true)



## Enrich

* Join external tables (merchant risk score, MCC codes, macro indicators).

#### Purpose: 
Add contextual information to enrich transactions and customer data.

![Join merchant risk score to transactions](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Join%20merchant%20risk%20score%20to%20transactions.JPG?raw=true)

* Feature engineering for churn/fraud:

#### Purpose:
 Create predictive features that capture customer behavior over time.

![Transactions in last 30 days per customer](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Transactions%20in%20last%2030%20days%20per%20customer.JPG?raw=true)


* Label churn = no tx in last X months ( X = 3/6)

#### Definition:
Churned customers are those with no transactions in the last X months. We can choose X = 3 or 6, depending on our business logic.

![Add churn label to customers](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Add%20churn%20label%20to%20customers.JPG?raw=true)

## Load to the analytics layer

* Store final models/tables: mart_customer_health, mart_fraud_alerts, mart_revenue_by_category.

  #### This means that we are moving our transformed and enriched data into the analytics layer, the layer where business users, BI tools (like Tableau/Power BI), or machine learning models can consume it easily.

#### We now have three key analytical tables (mart tables):

##### Table & purpose
* mart_customer_health:	Tracks customer activity, churn, engagement, and other behavioral metrics per customer

[![mart_customer_health table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/mart_customer_healt%20table.JPG?raw=true)](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/mart_customer_healt%20table.JPG)

* mart_fraud_alerts:    Stores flagged suspicious transactions or high-risk customers for fraud monitoring

[![Fraud alert table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Fraud%20alert%20table.JPG?raw=true)](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Fraud%20alert%20table.JPG)

* mart_revenue_by_category: Aggregated revenue metrics per merchant category, per month or year

  [![Revenue by category table](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/mart%20revenue%20bt%20category.JPG?raw=true)](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/mart%20revenue%20bt%20category.JPG)
  





### ETL Orchestration & Scheduling

* Use Windows task scheduler: schedule daily ingestion, dbt models run after load, and tests.

* Track DAG run statuses & SLAs.
#### At this stage of Orchestration & Scheduling, we are making our ETL workflow automatic, reliable, and monitorable.

### Purpose of Orchestration & Scheduling

* Orchestration: Control the order in which ETL tasks run (load → transform → aggregate → tests → dashboards).

* Scheduling: Decide when these tasks run (daily, hourly, weekly).

* Monitoring: Track if tasks succeed or fail and alert if something goes wrong.

### Tool: 
* Windows task scheduler (for automating daily runs)


### Automate everything daily 

![Task schedule screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Task%20schedule%20screenshot%201prefer.JPG)



![Task schedule screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Task%20schedule%20screenshot%202.JPG)


![Task schedule screenshot](https://github.com/CelesNeba/Financial-ETL-pipeline-and-dashboard/blob/main/Task%20schedule%20screenshot%203.JPG)



