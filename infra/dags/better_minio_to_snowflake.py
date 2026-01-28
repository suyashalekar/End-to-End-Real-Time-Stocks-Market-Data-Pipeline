from airflow import DAG
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from datetime import datetime, timedelta



# 1. Setup - Giving our "moving company" the addresses
S3_BUCKET = "bronze-transcations" # The "From" address
SNOWFLAKE_TABLE = "BRONZE_STOCK_QUOTES_RAW" # The "To" address

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 9, 9),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    "better_minio_to_snowflake",
    default_args=default_args,
    schedule_interval="*/1 * * * *", 
    catchup=False,
) as dag:

    # 2. The Task - This one block replaces ALL your old functions!
    transfer_data = S3ToSnowflakeOperator(
        task_id="move_data_to_snowflake",
        s3_bucket=S3_BUCKET,
        s3_keys=None, # This tells it to grab everything in the bucket
        snowflake_conn_id="snowflake_conn", # Connection saved in Airflow UI
        aws_conn_id="minio_conn",           # Connection saved in Airflow UI
        table=SNOWFLAKE_TABLE,
        schema="COMMON",
        database="STOCKS_MDS",
        file_format="(TYPE = 'JSON')",
        stage_type="s3", # MinIO works just like S3
    )