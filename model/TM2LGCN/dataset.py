from dataloader import load_data

import gensim
from gensim.corpora import Dictionary
from collections import defaultdict

import pickle
import scipy.sparse as sp
import numpy as np
import random
import torch


class MakeTMDataSet():
    def __init__(self):
        self.item2idx , self.df = load_data()
        
        self.df["item_idx"] = self.df["item"].map(self.item2idx)   
        self.df['item_name'] = self.df['item'].map(self.item2name())
        
        # inter_dict & df user 순서 주의
        self.inter_dict = self.df.groupby('user', sort=False)['item_name'].apply(set).apply(list).to_dict()
        self.user_ids = list(self.inter_dict.keys())
        self.user2idx = {user_id: index for index, user_id in enumerate(self.user_ids)}
        
        self.df["user_idx"] = self.df["user"].map(self.user2idx)
        
        self.num_item, self.num_user = len(self.item2idx), len(self.user2idx)
        
        self.dictionary, self.corpus = self.TM_traindata()
        
    def item2name(self):
        with open('/home/user/pickle/product_info_df.pickle', 'rb') as fr:
            product_info = pickle.load(fr)
            
        product_data = product_info.copy()
        product_data['title'] = product_data['title'].map(lambda x: x.replace("'",'').replace(',','').replace('(', ' ').replace(')', ' '))
        product_data['title'] = product_data['title'].map(lambda x: x.lower())
        product_data['title'] = product_data['title'].map(lambda x: x.split(' '))
        product_data['title'] = product_data['title'].map(lambda x: ' '.join(x).split())
        product_data['title'] = product_data['title'].map(lambda x: ' '.join(x))
        
        dict_products = product_data[['id','title']].set_index('id').to_dict()['title']
        
        return dict_products
    
    def TM_traindata(self):
        documents = list(self.inter_dict.values())
        dictionary = Dictionary(documents)
        corpus = [dictionary.doc2bow(document) for document in documents]
        return dictionary, corpus
    
    def get_dictionary(self):
        return self.dictionary
    
    def get_corpus(self):
        return self.corpus
    

class MakeLightGCNDataSet():
    def __init__(self, TM_dataset, lda_model, args):
        self.args = args
        self.TM_dataset = TM_dataset
        self.lda_model = lda_model
        
        self.df = self.TM_dataset.df
        self.user2idx = self.TM_dataset.user2idx
        self.item2idx = self.TM_dataset.item2idx
        self.num_user, self.num_item = self.TM_dataset.num_user, self.TM_dataset.num_item
        
        self.exist_users = [i for i in range(self.num_user)]
        self.exist_items = [i for i in range(self.num_item)]
        
        self.user_train, self.user_valid = self.generate_sequence_data()
        self.R_train, self.R_valid, self.R_total = self.generate_dok_matrix()
        self.ngcf_adj_matrix = self.generate_ngcf_adj_matrix()
        
        self.user_topic_tensor = self.get_TM_user_vector()
        
        self.n_train = len(self.R_train)
        self.batch_size = self.args.batch_size
        
    def generate_sequence_data(self) -> dict:
        """
        split train/valid
        중복 허용
        """
        users = defaultdict(list)
        user_train = {}
        user_valid = {}
        for user, item, time in zip(self.df['user_idx'], self.df['item_idx'], self.df['time']):
            users[user].append(item)
        
        for user in users:
            np.random.seed(self.args.seed)
            user_total = users[user]
            valid_indices = random.sample(range(len(user_total)), 2)
            valid = [user_total[idx] for idx in valid_indices]
            train = [user_total[idx] for idx in range(len(user_total)) if idx not in valid_indices]
            user_train[user] = train
            user_valid[user] = valid
        
        return user_train, user_valid
    
    def generate_dok_matrix(self):
        R_train = sp.dok_matrix((self.num_user, self.num_item), dtype=np.float32)
        R_valid = sp.dok_matrix((self.num_user, self.num_item), dtype=np.float32)
        R_total = sp.dok_matrix((self.num_user, self.num_item), dtype=np.float32)
        user_list = self.exist_users   # user2idx에 있는 value값
        for user in user_list:
            train_items = self.user_train[user]
            valid_items = self.user_valid[user]
            
            for train_item in train_items:
                R_train[user, train_item] = 1.0
                R_total[user, train_item] = 1.0
            
            for valid_item in valid_items:
                R_valid[user, valid_item] = 1.0
                R_total[user, valid_item] = 1.0
        
        return R_train, R_valid, R_total

    def generate_ngcf_adj_matrix(self):
        adj_mat = sp.dok_matrix((self.num_user + self.num_item, self.num_user + self.num_item), dtype=np.float32)
        adj_mat = adj_mat.tolil() # to_list
        R = self.R_train.tolil()

        adj_mat[:self.num_user, self.num_user:] = R
        adj_mat[self.num_user:, :self.num_user] = R.T
        adj_mat = adj_mat.todok() # to_dok_matrix

        def normalized_adj_single(adj):
            rowsum = np.array(adj.sum(1))
            d_inv = np.power(rowsum, -.5).flatten()  
            d_inv[np.isinf(d_inv)] = 0.
            d_mat_inv = sp.diags(d_inv)
            norm_adj = d_mat_inv.dot(adj).dot(d_mat_inv)

            return norm_adj.tocoo()

        ngcf_adj_matrix = normalized_adj_single(adj_mat)
        return ngcf_adj_matrix.tocsr()

    def get_TM_user_vector(self):
        user_topic_matrix = np.zeros((self.num_user, self.args.num_topics))
        corpus = self.TM_dataset.get_corpus()
        
        user_topic_vectors = [self.lda_model.get_document_topics(bow, minimum_probability=0.0) 
                              for bow in corpus]
        for i, user_vec in enumerate(user_topic_vectors):
            """
                i: user idx
                user_vec: (topic, prob)
            """
            for topic, prob in user_vec:
                user_topic_matrix[i, topic] = prob

        # numpy array --> torch tensor
        user_topic_tensor = torch.tensor(user_topic_matrix, dtype=torch.float32)
        
        return user_topic_tensor

    def sampling(self):
        users = random.sample(self.exist_users, self.args.batch_size)

        def sample_pos_items_for_u(u, num):
            pos_items = self.user_train[u]
            pos_batch = random.sample(pos_items, num)
            return pos_batch
        
        def sample_neg_items_for_u(u, num):
            neg_items = list(set(self.exist_items) - set(self.user_train[u]))
            neg_batch = random.sample(neg_items, num)
            return neg_batch
        
        pos_items, neg_items = [], []
        for user in users:
            pos_items += sample_pos_items_for_u(user, 1)
            neg_items += sample_neg_items_for_u(user, 1)
        
        return users, pos_items, neg_items
        
    def get_train_valid_data(self):
        return self.user_train, self.user_valid

    def get_R_data(self):
        return self.R_train, self.R_valid, self.R_total

    def get_ngcf_adj_matrix_data(self):
        return self.ngcf_adj_matrix