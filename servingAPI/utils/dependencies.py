import pickle
from .config import config
from .model import SASRec
import mlflow
from google.oauth2 import service_account
from google.cloud import storage
import torch

STORAGE_PATH = config.storage_path
SERVICE_ACCOUNT_FILE = config.account_json_path
PROJECT_ID = config.project_id
BUCKET_NAME = config.bucket_name
ARTIFACT_URI = config.artifact_uri
RUN_ID = config.run_id

dtm_user, user_idx, vectorizer = None, None, None

model = None

# using for parameter logging
client = mlflow.tracking.MlflowClient()
run_info = client.get_run(RUN_ID)

def download_model():
    # Download model artifacts
    mlflow.artifacts.download_artifacts(artifact_uri=ARTIFACT_URI, dst_path=STORAGE_PATH)


def get_model_num_params():
    num_user = run_info.data.params["num_user"]
    num_item = run_info.data.params["num_item"]
    
    return int(num_user), int(num_item)


def load_model():
    global model
    # download_model_path="/home/user/servingAPI/storage/model/data/model.pth"
    num_user, num_item = get_model_num_params()
    model = SASRec(num_user, num_item, 50, 1,
                   2, 10, 0.5, "cpu")
    
    download_model_path = "../storage/model/data/model.pth"
    model.load_state_dict(torch.load(download_model_path))


# def load_model():
#     import mlflow
#     global model
#     model = mlflow.pytorch.load_model(model_uri="s3://mlflow/9c5dfe82b5e744a7bc2087e63113c9c6/artifacts/model/MLmodel")
    
def get_model():
    global model
    return model


def load_dics(): 
    # LOAD ITEM2IDX PICKLE
    
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)

    item2idx_name = '240320/item_to_idx.pickle'

    blob_item2idx = bucket.blob(item2idx_name)

    global item2idx
    with blob_item2idx.open(mode='rb') as f:
        item2idx = pickle.load(f)

    return item2idx


def load_user_vector():
    # LOAD USER VECTOR
    global dtm_user
    with open(STORAGE_PATH + '/240320_tfidf_user_vector.pickle','rb') as fw:
        dtm_user = pickle.load(fw)
    return dtm_user
    
def load_user_index():
    # LOAD USER INDEX
    global user_idx
    with open(STORAGE_PATH + '/240320_tfidf_user_idx.pickle','rb') as fw:
        user_idx = pickle.load(fw)
    return user_idx
    

def load_vectorizer():
    # LOAD VECTORIZER
    global vectorizer
    with open(STORAGE_PATH + '/240320_tfidf_vectorizer.pickle','rb') as fw:
        vectorizer = pickle.load(fw)
    return vectorizer

def get_tfidf_dependencies():
    global dtm_user, user_idx, vectorizer
    return dtm_user, user_idx, vectorizer
    