from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default settings applied to all tasks in this DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    'network_threat_ingestion',
    default_args=default_args,
    description='Automated GDPR-compliant network traffic ingestion', 
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 3, 16),
    catchup=False,
    tags=['security', 'gdpr_compliant'],
) as dag:
    
    # Task 1: Run Python Script
    # Use Python3 and absolute container paths since Airflow runs on Linux in Docker
    run_ingestion = BashOperator(
        task_id='execute_extract_load_script',
        bash_command='python3 /opt/airflow/scripts/extract_load.py',
    )

    run_ingestion