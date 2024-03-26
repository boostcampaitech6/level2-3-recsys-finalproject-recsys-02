import pandas as pd
import numpy as np
import pickle
from args import args
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def tfidf(args):
    """
    ----------
    TF-IDF 연산 함수
    ----------
    """
    ## DATA LOAD
    print('--------------- Load Data ---------------')
    with open(args.save_path + 'df_grouped.pickle','rb') as fw:
        df_grouped = pickle.load(fw)

    ## TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_user = vectorizer.fit_transform(df_grouped['product_titles'])
    dtm_user = np.array(tfidf_user.todense())

    new_item = args.new_item
    new_product = vectorizer.transform([new_item])
    dtm_new = np.array(new_product.todense())

    # CALCULATE COSINE SIMILARITY
    cosine_similarities = cosine_similarity(dtm_user, dtm_new)
    sim = pd.DataFrame(cosine_similarities)

    # SIMILAR USER
    user_idx = {i:df_grouped.loc[i,'hashed_ip'] for i in range(len(df_grouped))}
    sim.index = sim.index.map(user_idx)
    result = sim.loc[args.user, 0]

    return result

tfidf(args)