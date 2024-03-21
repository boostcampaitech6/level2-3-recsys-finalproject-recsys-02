from google.oauth2 import service_account
from google.cloud import storage
import pickle

import torch
import numpy as np

from args import parse_args

def load_dics(): # item2idx, idx2item Pickle load
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

    blob_item2idx = bucket.blob(item2idx_name)

    with blob_item2idx.open(mode='rb') as f:
        item2idx = pickle.load(f)

    return item2idx

def seq_prepare(item_seq: list, candidates: list, max_len: int):
    item2idx = load_dics() ######pickle 파일
    item_seq = [(item2idx[key] if key in item2idx.keys() else 0) for key in item2idx] # dictionary에 없는 아이템은 0으로 indexing
    candidates = [(item2idx[key] if key in item2idx.keys() else 0) for key in item2idx] # dictionary에 없는 아이템..? 받으면 안되지 않나?

    seq = np.zeros([max_len], dtype=np.int32)
    idx = max_len - 1
    for i in reversed(item_seq):
        seq[idx] = i
        idx -= 1
        if idx == -1: break
    
    return seq, candidates



def test(model, item_seq, candidates, args): ## 여기서 args.maxlen = 10만 쓰는데 굳이...?
    
    #######모델 불러오기
    model.eval()

    seq, candidates= seq_prepare(item_seq = item_seq, candidates=candidates, max_len=args.max_len)

    with torch.no_grad():
        predictions = model.predict(np.array([seq]), np.array(candidates))

    return predictions

def main(args):
    

if __name__ == "__main__":
    args = parse_args()
    main(args)