# etl_pipeline_full_mysql.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime

print("🚀 Starting ETL pipeline run...")
print(f"Run started at: {datetime.now()}")

# --------------------------
# MySQL connection parameters
# --------------------------
db_user = 'root'
db_password = 'Remy2000123%40%40'
db_host = 'localhost'
db_port = '3306'
db_name = 'financial_etl_db'

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# --------------------------
# Load raw CSV file
# --------------------------
csv_path = r"D:\Backup C\Desktop\MY LESSONS\DATA ANALYTICS\financial_transactions_2000.csv"
df_raw = pd.read_csv(csv_path, parse_dates=['account_open_date', 'transaction_date'])

# --------------------------
# Basic transformations
# --------------------------
df_raw['transaction_month'] = df_raw['transaction_date'].dt.to_period('M').astype(str)
df_raw['transaction_dayofweek'] = df_raw['transaction_date'].dt.day_name()
df_raw['is_large_tx'] = np.where(df_raw['amount'] > 1000, 1, 0)
df_raw['amount_log'] = np.log1p(df_raw['amount'])
df_raw['year'] = df_raw['transaction_date'].dt.year

# --------------------------
# Separate tables
# --------------------------
raw_transactions = df_raw.copy()
clean_transactions = df_raw[['transaction_id', 'customer_id', 'transaction_date', 'transaction_type',
                             'amount', 'merchant', 'merchant_category', 'channel', 'balance_after', 'is_fraud']].copy()
fact_transactions = clean_transactions.copy()
dim_customers = df_raw[['customer_id', 'age', 'gender', 'annual_income', 'account_open_date',
                        'credit_score', 'segment']].drop_duplicates().copy()
merchant_category_map = df_raw[['merchant', 'merchant_category']].drop_duplicates().copy()

# Example placeholders for other tables
# You can add more transformations for agg_customer_monthly, mart_fraud_alerts, etc.
agg_customer_monthly = pd.DataFrame()  # placeholder
mart_fraud_alerts = pd.DataFrame()     # placeholder
mart_customer_health = pd.DataFrame()  # placeholder
mart_revenue_by_category = pd.DataFrame()  # placeholder

tables = {
    'raw_transactions': raw_transactions,
    'clean_transactions': clean_transactions,
    'fact_transactions': fact_transactions,
    'dim_customers': dim_customers,
    'merchant_category_map': merchant_category_map,
    'agg_customer_monthly': agg_customer_monthly,
    'mart_fraud_alerts': mart_fraud_alerts,
    'mart_customer_health': mart_customer_health,
    'mart_revenue_by_category': mart_revenue_by_category
}

# --------------------------
# Function to upsert tables
# --------------------------
def upsert_table(df, table_name, primary_keys=None):
    if df.empty:
        print(f"⚠️ Table {table_name} is empty, skipping...")
        return
    
    # Convert Period objects to string if present
    for col in df.columns:
        if pd.api.types.is_period_dtype(df[col]):
            df[col] = df[col].astype(str)
    
    with engine.begin() as conn:  # automatic commit/rollback
        for _, row in df.iterrows():
            # Construct REPLACE INTO SQL dynamically
            cols = row.index.tolist()
            placeholders = ', '.join([f":{c}" for c in cols])
            sql = f"REPLACE INTO {table_name} ({', '.join(cols)}) VALUES ({placeholders})"
            conn.execute(text(sql), row.to_dict())
    
    print(f"✅ Upserted table: {table_name}")

# --------------------------
# Run upsert for all tables
# --------------------------
for table_name, df_table in tables.items():
    upsert_table(df_table, table_name)

print("🏁 ETL pipeline completed successfully!")
print(f"Run finished at: {datetime.now()}")
