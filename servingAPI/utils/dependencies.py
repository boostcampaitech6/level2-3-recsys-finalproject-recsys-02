import pickle
from .config import config
from .model import SASRec
import mlflow
from google.oauth2 import service_account
from google.cloud import storage
import torch
import pandas as pd

STORAGE_PATH = config.storage_path
SERVICE_ACCOUNT_FILE = config.account_json_path
PROJECT_ID = config.project_id
BUCKET_NAME = config.bucket_name
MODEL_PATH = config.download_model_path

df_grouped = None

item2idx, model = None, None

similarity_matrix = None

def get_model_arch():
    max_len = 10
    hidden_units = 50
    num_heads = 1
    num_layers = 2
    dropout_rate=0.5
    num_workers = 1
    #device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'
    # training setting
    num_user, num_item = 33075, 12069
    global model
    model = SASRec(num_user, num_item, hidden_units, num_heads, num_layers, max_len, dropout_rate, device)
    return model


def load_model():
    global model
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    model_path = '240320/SASRec.pt'
    blob = bucket.get_blob(model_path)
    blob.download_to_filename(STORAGE_PATH + '/SASRec.pt')
    model = get_model_arch()
    model.load_state_dict(torch.load(STORAGE_PATH + '/SASRec.pt', map_location=torch.device('cpu')))
    model.eval()
    print(model)

    
def get_model():
    global model
    return model


def load_dict(): 
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


def get_item2idx():
    global item2idx
    return item2idx


def load_df_grouped():
    # LOAD DF_GROUPED
    global df_grouped
    with open(STORAGE_PATH + '/240320_df_grouped.pickle','rb') as fw:
        df_grouped = pickle.load(fw)
    return df_grouped

def get_df_grouped():
    global df_grouped
    return df_grouped
    
def load_similarity_matrix() -> pd.DataFrame:
    # LOAD SIMILARITY MATRIX
    global similarity_matrix
    with open(STORAGE_PATH + '/item_similarity.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)
    

def get_similarity_matrix():
    global similarity_matrix
    return similarity_matrix