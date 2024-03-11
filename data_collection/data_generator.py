import os
import pandas as pd
import json
import time
from google.cloud import storage, bigquery
from google.oauth2 import service_account
from notiAPI.api import NotiServerRequest

# 상수 정의
DATA_DIR = "../data/"
CONFIG_DIR = "../config/"

PROJECT_ID = "level3-416207"
BQ_SERVICE_ACCOUNT_FILE = "level3-416207-893f91c9529e.json"

GCS_SERVICE_ACCOUNT_FILE = "level3-416207-b822e8eb3877.json"
GCS_BUCKET_NAME = "level3_recsys02"
GCS_DESTINATION_PREFIX = "product/"

def authenticate_gcs(credentials_path):
    """Google Cloud Storage 클라이언트 인증"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    return storage.Client(credentials=credentials)

def authenticate_bigquery(credentials_path):
    """Google Cloud BigQuery 클라이언트 인증"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)

def upload_blob(client, bucket_name, source_file_name, destination_blob_name):
    """파일을 Google Cloud Storage 버킷에 업로드"""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

def get_products(req_num = 1000):
    # CSV 파일 읽기 및 필터링
    product_df = pd.read_csv(os.path.join(DATA_DIR, "interaction_from_240113_replaced.csv"))
    product_df = product_df[~product_df["products"].str.contains("-")]
    product_idlst = product_df["products"].unique().tolist()

    # Google Cloud Storage 클라이언트 인증
    credentials_path = os.path.join(CONFIG_DIR, GCS_SERVICE_ACCOUNT_FILE)
    client = authenticate_gcs(credentials_path)

    # 제품 ID를 1000개씩 배치로 처리 최대 조회수가 1000개
    for i, num in enumerate(range(0, len(product_idlst), req_num)):
        source_file_name = os.path.join(DATA_DIR, f"product_info_{i}.json")
        product_ids = product_idlst[num:num + req_num]

        print(i + 1, len(product_ids)) # 횟수 확인
        
        # API에서 제품 정보 가져오기
        res = NotiServerRequest.bulk_product_info(ids=product_ids)
        data = res.json()

        # JSON 파일에 제품 정보 쓰기
        with open(source_file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent="\t", ensure_ascii=False)

        # JSON 파일 Google Cloud Storage에 업로드
        destination_blob_name = os.path.join(GCS_DESTINATION_PREFIX, f"product_info_{i}.json")
        upload_blob(client, GCS_BUCKET_NAME, source_file_name, destination_blob_name)
    
        # 속도 제한을 위해 실행 일시 중지
        time.sleep(60)
        
def get_users():
    # Google Cloud Storage 클라이언트 인증
    gs_credentials_path = os.path.join(CONFIG_DIR, GCS_SERVICE_ACCOUNT_FILE)
    gs_client = authenticate_gcs(gs_credentials_path)

    # Authenticate Google Cloud Storage client
    bq_credentials_path = os.path.join(CONFIG_DIR, BQ_SERVICE_ACCOUNT_FILE)
    bq_client = authenticate_bigquery(bq_credentials_path)
    
    # 쿼리 실행 / 데이터웨어하우스에서 데이터 불러오기
    # 빅쿼리 디렉토리는 <프로젝트ID>.<데이터셋ID>.<테이블ID> 순으로 저장되어있음
    QUERY = (
        '''
        SELECT  DISTINCT user_device_endpoint FROM `level3-416207.log_129.revised_log_129`
        WHERE user_device_endpoint IS NOT NULL
        ''')

    # API request
    df = bq_client.query(QUERY).to_dataframe()
    user_device_list = df['user_device_endpoint'].tolist()
    
    source_file_name = os.path.join(DATA_DIR, f"user_info.json")
    res = NotiServerRequest.bulk_user_info(ids=user_device_list)
    data = res.json()
    
    # JSON 파일에 제품 정보 쓰기
    with open(source_file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent="\t", ensure_ascii=False)
        
    # JSON 파일 Google Cloud Storage에 업로드
    destination_blob_name = os.path.join(GCS_DESTINATION_PREFIX, f"user_device_info.json")
    upload_blob(gs_client, GCS_BUCKET_NAME, source_file_name, destination_blob_name)


if __name__ == "__main__":
    get_products(req_num=1000) # req_num: 한번 요청시 조회수
    get_users()

