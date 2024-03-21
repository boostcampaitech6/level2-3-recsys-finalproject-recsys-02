import pandas as pd
import numpy as np
import pickle
import argparse
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime



# BASIC ENVIRONMENT SETUP
parser = argparse.ArgumentParser(description='parser')
arg = parser.add_argument
arg('--user', type=str, default='', help='유사도 계산이 필요한 user의 ip/endpoint를 넣습니다. 현재는 hashed_ip를 넣습니다.')
arg('--save_vector_path', type=str, default='../asset/', help='User vector를 저장할 path를 설정할 수 있습니다.')
arg('--new_item', type=str, default='', help='새로운 상품의 title을 받습니다.')
args = parser.parse_args()


def inference(args):
        # LOAD VECTORIZER
    with open(args.save_vector_path + 'tfidf_vectorizer.pickle','rb') as fw:
        vectorizer = pickle.load(fw)


    # LOAD USER VECTOR
    with open(args.save_vector_path + 'tfidf_user_vector.pickle','rb') as fw:
        dtm_user = pickle.load(fw)


    # LOAD USER INDEX
    with open(args.save_vector_path + 'tfidf_user_idx.pickle','rb') as fw:
        user_idx = pickle.load(fw)


    # NEW ITEM VECTORIZING
    new_item = args.new_item
    new_product = vectorizer.transform([new_item])
    dtm_new = np.array(new_product.todense())


    # CALCULATE COSINE SIMILARITY
    cosine_similarities = cosine_similarity(dtm_user, dtm_new)
    sim = pd.DataFrame(cosine_similarities)


    # SIMILAR USER
    sim.index = sim.index.map(user_idx)
    result = sim.loc[args.user, 0]

    return result


inference(args)