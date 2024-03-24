import pandas as pd
import numpy as np
import torch
import pickle
from sklearn.metrics.pairwise import cosine_similarity

STORAGE_PATH = ''
def tfidf_inference(user, item, dtm_user, user_idx, vectorizer):
    new_product = vectorizer.transform([item])
    dtm_new = np.array(new_product.todense())


    # CALCULATE COSINE SIMILARITY
    cosine_similarities = cosine_similarity(dtm_user, dtm_new)
    sim = pd.DataFrame(cosine_similarities)


    # SIMILAR USER
    sim.index = sim.index.map(user_idx)
    result = sim.loc[user, 0]

    return result


def seq_prepare(item_seq: list, candidates: list, max_len: int):
    global item2idx
    item_seq = [(item2idx[key] if key in item2idx.keys() else 0) for key in item2idx] # dictionary에 없는 아이템은 0으로 indexing
    candidates = [(item2idx[key] if key in item2idx.keys() else 0) for key in item2idx] # dictionary에 없는 아이템..? 받으면 안되지 않나?

    seq = np.zeros([max_len], dtype=np.int32)
    idx = max_len - 1
    for i in reversed(item_seq):
        seq[idx] = i
        idx -= 1
        if idx == -1: break

    return seq, candidates


def test(model, item_seq, candidates):
    model.eval()

    seq, candidates= seq_prepare(item_seq = item_seq, candidates=candidates, max_len=10)

    with torch.no_grad():
        predictions = model.predict(np.array([seq]), np.array(candidates))

    return predictions.tolist()[0]