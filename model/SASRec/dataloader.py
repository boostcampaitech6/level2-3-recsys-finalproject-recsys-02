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

    # user별 interaction 개수를 계산
    user_interaction_counts = df['user'].value_counts()

    # interaction이 3개 이상인 user의 목록을 가져옴
    selected_users = user_interaction_counts[user_interaction_counts >= 3].index

    # interaction이 3개 이상인 user에 대한 데이터만 남김
    df = df[df['user'].isin(selected_users)]

    return df # user, item가 예쁘게 정렬되어 있는 interaction data


def data_load(args):
    SERVICE_ACCOUNT_FILE = "../config/level3-416207-893f91c9529e.json"

    # Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

    # 스토리지 클라이언트 객체 생성
    project_id = "level3-416207"
    storage_client = storage.Client(credentials=credentials, project=project_id)

    # 버킷 및 블롭(객체) 설정
    bucket_name = 'crwalnoti'
    bucket = storage_client.bucket(bucket_name)

    item2idx_name = '240320/item_to_idx.pickle'
    inter_name = '240320/inter_240129.csv'

    blob_item2idx = bucket.blob(item2idx_name)

    with blob_item2idx.open(mode='rb') as f:
        item2idx = pickle.load(f)
    
    blob_inter = bucket.blob(inter_name)
    with blob_inter.open(mode='rb') as f:
        interaction_df = pd.read_csv(f)

    interaction_df = preprocess(interaction_df) # user, item

    item_ids = interaction_df['item'].unique()
    user_ids = interaction_df['user'].unique()
    num_item, num_user = len(item2idx), len(user_ids)
    num_batch = num_user // args.batch_size
    user2idx = pd.Series(data=np.arange(len(user_ids)), index=user_ids) # user re-indexing (0~num_user-1)

    # dataframe indexing
    interaction_df['item_idx'] = interaction_df['item'].map(item2idx)
    interaction_df = pd.merge(interaction_df, pd.DataFrame({'user': user_ids, 'user_idx': user2idx[user_ids].values}), on='user', how='inner')
    interaction_df.sort_values(['user_idx', 'time'], inplace=True)
    del interaction_df['item'], interaction_df['user']

    # train set, valid set 생성
    users = defaultdict(list) # defaultdict은 dictionary의 key가 없을때 default 값을 value로 반환
    user_train = {}
    user_valid = {}
    for u, i, t in zip(interaction_df['user_idx'], interaction_df['item_idx'], interaction_df['time']):
        users[u].append(i)

    for user in users:
        user_train[user] = users[user][:-1]
        user_valid[user] = [users[user][-1]]
    
    return user_train, user_valid, num_item, num_user, num_batch

