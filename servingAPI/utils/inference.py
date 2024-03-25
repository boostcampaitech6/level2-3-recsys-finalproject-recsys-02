import pandas as pd
import numpy as np
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