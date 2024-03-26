import pandas as pd
import numpy as np
import torch
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .dependencies import get_item2idx, get_df_grouped

STORAGE_PATH = ''
def tfidf_inference(user, item):
    df_grouped = get_df_grouped()
    ## TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_user = vectorizer.fit_transform(df_grouped['product_titles'])
    dtm_user = np.array(tfidf_user.todense())

    new_item = item
    new_product = vectorizer.transform([new_item])
    dtm_new = np.array(new_product.todense())

    # CALCULATE COSINE SIMILARITY
    cosine_similarities = cosine_similarity(dtm_user, dtm_new)
    sim = pd.DataFrame(cosine_similarities)

    # SIMILAR USER
    user_idx = {i:df_grouped.loc[i,'hashed_ip'] for i in range(len(df_grouped))}
    sim.index = sim.index.map(user_idx)
    result = sim.loc[user, 0]

    return result


def seq_prepare(item_seq: list, candidates: list, max_len: int):
    item2idx = get_item2idx()
    item_seq = [(item2idx[key] if key in item2idx.keys() else 0) for key in item_seq] # dictionary에 없는 아이템은 0으로 indexing
    candidates = [(item2idx[key] if key in item2idx.keys() else 0) for key in candidates] # dictionary에 없는 아이템..? 받으면 안되지 않나?

    seq = np.zeros([max_len], dtype=np.int32)
    idx = max_len - 1
    for i in reversed(item_seq):
        seq[idx] = i
        idx -= 1
        if idx == -1: break

    return seq, candidates


def sasrec_inference(model, item_seq, candidates):
    model.eval()

    seq, candidates= seq_prepare(item_seq = item_seq, candidates=candidates, max_len=10)

    with torch.no_grad():
        predictions = model.predict(np.array([seq]), np.array(candidates))

    return predictions.tolist()[0]


def ibcf_inference(item_similarity_df: pd.DataFrame, item: str, topn: int = 5) -> pd.DataFrame:
    topn = topn + 1  # 입력한 아이템 제외
    if item in item_similarity_df.index:
        sim_item_df = item_similarity_df[item].sort_values(ascending=False).reset_index().rename(columns={'index':'item',item:'similarity'})
        print('입력한 아이템 id:', item)
        return sim_item_df[1:topn]
    else:
        print('아이템 id를 다시 확인해주세요')
        return None