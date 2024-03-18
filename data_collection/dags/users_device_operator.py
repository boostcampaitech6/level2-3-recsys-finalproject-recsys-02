from airflow import DAG
from datetime import datetime, timedelta
from pathlib import Path
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator # GCS 데이터를 BigQuery로 옮김
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator # BigQuery에서 Query를 실행
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator # Local에서 GCS로 데이터를 옮김


PROJECT_ID = "level3-416207" # 프로젝트 ID
BUCKET_NAME = "crwalnoti" # 업로드할 GCS Bucket
FILE_NAME = "users_device_info.csv" 
LOCAL_FILE_PATH = str(Path(__file__).parent.parent / "data" / FILE_NAME) # Composer와 연결된 GCS의 경로

GCS_PATH = f"user_info/users_device_info.csv" # 업로드할 GCS(BigQuert와 연결된)의 경로

default_args = {
    "owner": "czero",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 7),
    "end_date": datetime(2024, 3, 12)
}


# GCS에서 BigQuery에 적재하기전 스키마 설정 
schema_fields = [
  {
    "mode": "NULLABLE",
    "name": "id",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "keywords",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "favorite_ids",
    "type": "STRING"
  },
]

with DAG(
    dag_id="elt-users_info",
    default_args=default_args,
    schedule_interval="30 0 * * *",
    tags=["user"],
    catchup=True
) as dag:
    
    # 1) Extract : Local To GCS
    extract_data = LocalFilesystemToGCSOperator(
        task_id="extract_data",
        src=LOCAL_FILE_PATH,
        dst=GCS_PATH,
        bucket=BUCKET_NAME
    )
    
    # 2) Load : GCS To BigQuery
    load_csv = GCSToBigQueryOperator(
        task_id="gcs_to_bigquery",
        bucket=BUCKET_NAME,
        source_objects=[GCS_PATH],
        destination_project_dataset_table=f"{PROJECT_ID}.log_129.user_device", # from GCS to BigQuery 
        schema_fields=schema_fields,
        source_format='CSV',
        skip_leading_rows=1,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        # location="US"
    )
    
    # 3) Transform : BigQuery에서 Query 실행해서 다시 BigQuery에 저장
    sql_query = f"""
    SELECT
      *
    FROM `{PROJECT_ID}.log_129.user_device`
    WHERE keywords IS NOT NULL
    AND favorite_ids IS NOT NULL;
    """
    transform = BigQueryExecuteQueryOperator(
        task_id="run_query",
        sql=sql_query,
        use_legacy_sql=False,
        allow_large_results=True,
        write_disposition="WRITE_TRUNCATE",
        destination_dataset_table=f"{PROJECT_ID}.log_129.user_device_notNULL"
    )

    extract_data >> load_csv >> transform