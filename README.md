# Airflow MinIO

Example of Airflow and MinIO (min.io) in Docker.
Shared in the hope it is helpful to somebody (not production ready etc., see LICENSE file for details).

## Running

### Commands
Have a look in the Makefile for commands. Only tested on Linux.
```shell
echo "Setting Airflow settings"
echo "AIRFLOW_UID=$(id -u)" > .env
echo "Please make sure the user id is correct in .env"
nano .env

echo "Starting everything"
echo "Please wait a while or run 'make ps' to see if things are 'ready' and the init containers have exited (finished)"
echo "Airflow: http://127.0.0.1:8080 (Username: 'airflow', Password: 'airflow')"
echo "Minio: http://127.0.0.1:9002 (Username: 'admin', Password: 'minio-password')"
echo "Ctrl+c to exit when ready"
make up
echo "Cleaning up / removing everything"
make stop
```

### UI
Example dag is in the UI. When you run it, have a look at the logs of print_s3_object.

## How it works
1. Creates a `minio/minio` (MinIO) container
2. Use MC inside `minio/mc` (`minio-init`) to create a bucket and upload a csv file (`import/minio/airflow/data.csv`)
3. The `airflow-provision` creates a connector in Airflow that allows Airflow to access MinIO.
4. Sample DAG to read the CSV file from MinIO

## Notes:
* S3 connector has been replaced with 'Amazon Web Services' connector

## Links / References
* https://www.youtube.com/watch?v=sVNvAtIZWdQ
* https://blog.min.io/apache-airflow-minio/
