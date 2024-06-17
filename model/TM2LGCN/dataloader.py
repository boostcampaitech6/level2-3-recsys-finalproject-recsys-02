from google.oauth2 import service_account
from google.cloud import storage
import pickle

from datetime import datetime
import pandas as pd
import numpy as np
from collections import defaultdict


def preprocess(df):
    df = df[df['uri_first']==1]
    df['timestamp']=pd.to_datetime(df['local_time']).astype(int)//10**9
    df = df[['hashed_ip', 'products', 'timestamp']]

    df['user']=df['hashed_ip']
    df['item']=df['products']
    df['time']=df['timestamp']

    df.sort_values(['user', 'timestamp'])

    del df['hashed_ip'], df['products'], df['timestamp']
    user_interaction_counts = df['user'].value_counts()
    selected_users = user_interaction_counts[user_interaction_counts >= 5].index
    df = df[df['user'].isin(selected_users)]

    return df


def load_data(): 
    # LOAD ITEM2IDX PICKLE
    SERVICE_ACCOUNT_FILE = "../config/level3-416207-893f91c9529e.json"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    project_id = "level3-416207"
    storage_client = storage.Client(credentials=credentials, project=project_id)
    bucket_name = 'crwalnoti'
    bucket = storage_client.bucket(bucket_name)

    item2idx_name = '240320/item_to_idx.pickle'
    inter_name = '240320/inter_240129.csv'

    # prepare item2idx
    blob_item2idx = bucket.blob(item2idx_name)
    with blob_item2idx.open(mode='rb') as f:
        item2idx = pickle.load(f)
    
    # prepare interaction_df
    blob_inter = bucket.blob(inter_name)
    with blob_inter.open(mode='rb') as f:
        interaction_df = pd.read_csv(f)
        
    interaction_df = preprocess(interaction_df)

    return item2idx, interaction_df

