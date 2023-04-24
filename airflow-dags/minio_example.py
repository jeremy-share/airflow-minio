from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
import csv
import pprint
from datetime import datetime


def print_file():
    print("INFO: Running")
    s3_hook = S3Hook(aws_conn_id="myminio")
    obj = s3_hook.get_key(key="data.csv", bucket_name="airflow")
    s = obj.get()['Body'].read().decode('utf-8')
    lines = s.splitlines()
    pprint.pprint(lines)
    reader = csv.DictReader(lines)
    rows = list(reader)
    if not rows:
        print("CSV file has no data")
    else:
        pprint.pprint(rows)
    print("INFO: Finished")


with DAG(
    dag_id="minio_example",
    start_date=datetime.utcnow(),
    schedule_interval=None
) as dag:
    wait_for_file = S3KeySensor(
        task_id="wait_for_file",
        bucket_name="airflow",
        bucket_key="data.csv",
        timeout=60 * 60,
        aws_conn_id="myminio"
    )
    print_s3_object = PythonOperator(
        task_id="print_s3_object",
        python_callable=print_file
    )

    wait_for_file >> print_s3_object
