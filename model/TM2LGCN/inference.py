import pickle
import torch

from gensim.corpora import Dictionary
from gensim.models import LdaModel


def item2name():
    with open('../servingAPI/storage/product_info_df.pickle', 'rb') as fr:
        product_info = pickle.load(fr)
        
    product_data = product_info.copy()
    product_data['title'] = product_data['title'].map(lambda x: x.replace("'",'').replace(',','').replace('(', ' ').replace(')', ' '))
    product_data['title'] = product_data['title'].map(lambda x: x.lower())
    product_data['title'] = product_data['title'].map(lambda x: x.split(' '))
    product_data['title'] = product_data['title'].map(lambda x: ' '.join(x).split())
    product_data['title'] = product_data['title'].map(lambda x: ' '.join(x))
    
    dict_products = product_data[['id','title']].set_index('id').to_dict()['title']
    
    return dict_products


def make_UserVector(user_seq):
    model_path = "../servingAPI/storage/model/lda_model"
    dictionary_path = "../servingAPI/storage/dictionary"
    
    lda_model = LdaModel.load(model_path)
    dictionary = Dictionary.load(dictionary_path)
    
    dict_products = item2name()
    user_seq = [dict_products[i] for i in user_seq]
    
    new_user_bow = dictionary.doc2bow(user_seq)
    user_topic_distribution = lda_model.get_document_topics(new_user_bow)
    
    user_topic_vector = [prob for _, prob in user_topic_distribution]
    user_embedding = torch.tensor(user_topic_vector, dtype=torch.float).unsqueeze(0)
    
    return user_embedding


def inference(model, user_seq, item_seq, item2idx):
    model.eval()
    
    user_embedding = make_UserVector(user_seq)
    
    item_indices = [item2idx.get(item, 0) for item in item_seq]
    
    item_indices_tensor = torch.tensor(item_indices, dtype=torch.long)
    item_embeddings = model.weight_dict['item_embedding'][item_indices_tensor]
    
    scores = torch.matmul(user_embedding, item_embeddings.T).squeeze()
    preference_scores = torch.tanh(scores)
    
    scores_list = preference_scores.tolist()
    
    return scores_list