import pickle
from .config import config

STORAGE_PATH = config.storage_path

dtm_user, user_idx, vectorizer = None, None, None

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
    