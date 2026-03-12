# Import libraries
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

# extract market data
def extract_market_data():
    print("Extracting market data from API")

# store raw data
def store_raw_data():
    print("Saving raw market data to GCS raw layer")

# validate market data
def validate_market_data():
    print("Validating market data")

# load to bigquery
def load_to_bigquery():
    print("Loading validated data into BigQuery")

with DAG(
    dag_id="finstream_market_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["finstrea", "market-data"]
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_market_data",
        python_callable=extract_market_data
    )
    
    raw_task = PythonOperator(
        task_id="store_raw_data",
        python_callable=store_raw_data
    )
    
    validate_task = PythonOperator(
        task_id="validate_market_data",
        python_callable=validate_market_data
    )
    
    load_task = PythonOperator(
        task_id = "load_to_bigquery",
        python_callable=load_to_bigquery
    )
    
    extract_task >> raw_task >> validate_task >> load_task