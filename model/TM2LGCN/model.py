import numpy as np
import torch
import torch.nn as nn

class LightGCN(nn.Module):
    def __init__(self, n_users, n_items, args, adj_mtx, user_topic_tensor):
        super().__init__()
        # initialize Class attributes
        self.n_users = n_users
        self.n_items = n_items
        self.args = args
        self.emb_dim = self.args.emb_dim
        self.device = args.device
        
        self.l = adj_mtx   
        self.user_topic_tensor = user_topic_tensor.to(self.args.device)
        
        # PyTorch sparse tensor
        self.graph = self._convert_sp_mat_to_sp_tensor(self.l)

        self.reg = self.args.reg   
        self.n_layers = self.args.n_layers   
        self.node_dropout = self.args.node_dropout

        # Initialize weights
        # TM + Xavier
        self.weight_dict = self._init_weights()
        print("Weights initialized.")

    def _init_weights(self):
        print("Initializing weights...")
        weight_dict = nn.ParameterDict() 

        initializer = torch.nn.init.xavier_uniform_
        
        weight_dict['user_embedding'] = nn.Parameter(self.user_topic_tensor)
        weight_dict['item_embedding'] = nn.Parameter(initializer(torch.empty(self.n_items, self.emb_dim).to(self.device)))

        return weight_dict

    # convert sparse matrix into sparse PyTorch tensor
    def _convert_sp_mat_to_sp_tensor(self, X):
        """
        Convert scipy sparse matrix to PyTorch sparse matrix

        Arguments:
        ----------
        X = Adjacency matrix, scipy sparse matrix
        """
        coo = X.tocoo().astype(np.float32)
        i = torch.LongTensor(np.mat([coo.row, coo.col]))
        v = torch.FloatTensor(coo.data)   
        res = torch.sparse.FloatTensor(i, v, coo.shape).to(self.device)
        return res

    # apply node_dropout
    def _droupout_sparse(self, X):
        """
        Drop individual locations in X
        
        Arguments:
        ---------
        X = adjacency matrix (PyTorch sparse tensor)
        dropout = fraction of nodes to drop
        noise_shape = number of non non-zero entries of X
        """
        node_dropout_mask = ((self.node_dropout) + torch.rand(X._nnz())).floor().bool().to(self.device)
        i = X.coalesce().indices()   
        v = X.coalesce()._values()   
        i[:,node_dropout_mask] = 0   
        v[node_dropout_mask] = 0
        X_dropout = torch.sparse.FloatTensor(i, v, X.shape).to(self.device)

        return  X_dropout.mul(1/(1-self.node_dropout))

    def forward(self, u, i, j):
        """
        Computes the forward pass
        
        Arguments:
        ---------
        u = user
        i = positive item (user interacted with item)
        j = negative item (user did not interact with item)
        """
        # apply drop-out mask
        graph = self._droupout_sparse(self.graph) if self.node_dropout > 0 else self.graph

        ego_embeddings = torch.cat([self.weight_dict['user_embedding'], self.weight_dict['item_embedding']], 0)

        for k in range(self.n_layers):
            ego_embeddings = torch.sparse.mm(graph, ego_embeddings)
        
        u_emb, i_emb = ego_embeddings.split([self.n_users, self.n_items], 0)

        self.u_emb = u_emb
        self.i_emb = i_emb
        
        u_emb_batch = u_emb[u]  # (batch_size, emb_dim)
        pos_i_emb_batch = i_emb[i]  # (batch_size, emb_dim)
        neg_i_emb_batch = i_emb[j]  # (batch_size, emb_dim)
        

        # pos_scores & neg_scores
        pos_scores = torch.sum(u_emb_batch * pos_i_emb_batch, dim=1)  # (batch_size)
        neg_scores = torch.sum(u_emb_batch * neg_i_emb_batch, dim=1)  # (batch_size)
        
        # Concatenate pos & neg
        scores = torch.cat([pos_scores, neg_scores])  # (2*batch_size)
        labels = torch.cat([torch.ones_like(pos_scores), torch.zeros_like(neg_scores)])  # (2*batch_size)

        # Calculate BCEWithLogitsLoss
        loss_fn = torch.nn.BCEWithLogitsLoss()
        loss = loss_fn(scores, labels)

        return loss