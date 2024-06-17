from airflow import DAG
from datetime import datetime, timedelta
from pathlib import Path
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator  # GCS 데이터를 BigQuery로 옮김
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator  # BigQuery에서 Query를 실행
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator  # Local에서 GCS로 데이터를 옮김

execution_date = "{{ ds_nodash }}"  # 20240101

PROJECT_ID = "level3-416207"  # 프로젝트 ID
BUCKET_NAME = "crwalnoti"  # 업로드할 GCS Bucket

FILE_NAME = f"product_info_{execution_date}.csv"
LOCAL_FILE_PATH = str(Path(__file__).parent.parent / "data" / "products" / FILE_NAME)  # Composer와 연결된 GCS의 경로

GCS_PATH = f"products_info/product_info_{execution_date}.csv"  # 업로드할 GCS(BigQuert와 연결된)의 경로

default_args = {
    "owner": "czero",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 2),
    "end_date": datetime(2024, 2, 20)
}


# GCS에서 BigQuery에 적재하기전 스키마 설정
schema_fields = [
    {"name": "p_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "card_dc", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "brand", "type": "STRING", "mode": "NULLABLE"},
    {"name": "category_big", "type": "STRING", "mode": "NULLABLE"},
    {"name": "category_small", "type": "STRING", "mode": "NULLABLE"},
    {"name": "original_price", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "price", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
    {"name": "type", "type": "STRING", "mode": "NULLABLE"},
    {"name": "piv", "type": "STRING", "mode": "NULLABLE"}
]


with DAG(
        dag_id="elt-product_v5",
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
        destination_project_dataset_table=f"{PROJECT_ID}.log_129.products",  # from GCS to BigQuery
        schema_fields=schema_fields,
        source_format='CSV',
        skip_leading_rows=1,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
        # location="US"
    )

    # 3) Transform : BigQuery에서 Query 실행해서 다시 BigQuery에 저장
    # BigQuery에서 통계 정보를 계산하여 새로운 테이블에 저장
    sql_query = f"""
    SELECT
        COUNT(*) AS total_records,
        COUNT(DISTINCT p_id) AS unique_product_ids,
        AVG(IFNULL(price, 0)) AS average_price,
        MAX(IFNULL(price, 0)) AS max_price,
        MIN(IFNULL(price, 0)) AS min_price,
        COUNT(p_id IS NULL OR NULL) AS null_p_id_count,
        COUNT(card_dc IS NULL OR NULL) AS null_card_dc_count,
        COUNT(brand IS NULL OR NULL) AS null_brand_count,
        COUNT(category_big IS NULL OR NULL) AS null_category_big_count,
        COUNT(category_small IS NULL OR NULL) AS null_category_small_count,
        COUNT(original_price IS NULL OR NULL) AS null_original_price_count,
        COUNT(price IS NULL OR NULL) AS null_price_count,
        COUNT(title IS NULL OR NULL) AS null_title_count,
        COUNT(type IS NULL OR NULL) AS null_type_count,
        COUNT(piv IS NULL OR NULL) AS null_piv_count
    FROM `{PROJECT_ID}.log_129.products`
    """
        
    transform = BigQueryExecuteQueryOperator(
        task_id="run_query",
        sql=sql_query,
        use_legacy_sql=False,
        allow_large_results=True,
        write_disposition="WRITE_TRUNCATE",
        destination_dataset_table=f"{PROJECT_ID}.log_129.product_statistics"
    )

    # extract_data >> load_csv
    extract_data >> load_csv >> transform