import pandas as pd
import numpy as np
import pickle
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from data_loader import tfidf_data_load



## BASIC ENVIRONMENT SETUP
save_vector_path = '../../data/'


## DATA LOAD
print('--------------- Load Data ---------------')
df_grouped = tfidf_data_load()


## TF-IDF
vectorizer = TfidfVectorizer()
tfidf_user = vectorizer.fit_transform(df_grouped['product_titles'])
dtm_user = np.array(tfidf_user.todense())


## SAVE VECTORIZER
with open(save_vector_path + 'tfidf_vectorizer.pickle','wb') as fw: 
    pickle.dump(vectorizer, fw)


## SAVE USER VECTOR
with open(save_vector_path + 'tfidf_user_vector.pickle','wb') as fw:
    pickle.dump(dtm_user, fw)


## SAVE USER INDEX
user_idx = {i:df_grouped.loc[i,'hashed_ip'] for i in range(len(df_grouped))}
with open(save_vector_path + 'tfidf_user_idx.pickle','wb') as fw:
    pickle.dump(user_idx, fw)



print('Done!')