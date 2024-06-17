from args import parse_args
from Dataset import MakeTMDataSet, MakeLightGCNDataSet
from gensim.models import LdaModel
from model import LightGCN
from trainer import train, evaluate
from tqdm import tqdm

import torch
import os
import mlflow
import mlflow.pytorch

def main(args):

    print(f'----------------------Load TM Data & Make TM Dataset----------------------')
    TM_dataset = MakeTMDataSet()
    dictionary, corpus = TM_dataset.get_dictionary(), TM_dataset.get_corpus()
    print(f'Done.')
    
    print(f'----------------------Load & Train TM Model----------------------')
    print(f'...')
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, 
                   num_topics=args.num_topics, 
                   random_state=args.random_state, 
                   passes=args.passes)
    print(f'Done.')
    
    print(f'----------------------Make LGCN_dataset & LGCN_model----------------------')
    lightgcn_dataset = MakeLightGCNDataSet(TM_dataset, lda_model, args)
    ngcf_adj_matrix = lightgcn_dataset.get_ngcf_adj_matrix_data()
    R_train, R_valid, R_total = lightgcn_dataset.get_R_data()
    
    args.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = LightGCN(
                        n_users = lightgcn_dataset.num_user,
                        n_items = lightgcn_dataset.num_item,
                        args = args,
                        adj_mtx = ngcf_adj_matrix,
                        user_topic_tensor = lightgcn_dataset.user_topic_tensor,
                        ).to(args.device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    print(f'Done.')
    
    print(f'----------------------Training----------------------')
    best_hit = 0
    for epoch in range(1, args.num_epochs + 1):
        tbar = tqdm(range(1))
        for _ in tbar:
            train_loss = train(
                model = model, 
                make_graph_data_set = lightgcn_dataset, 
                optimizer = optimizer,
                n_batch = args.n_batch,
                )
            with torch.no_grad():
                ndcg, hit = evaluate(
                    u_emb = model.u_emb.detach(), 
                    i_emb = model.i_emb.detach(), 
                    Rtr = R_train, 
                    Rte = R_valid, 
                    args = args,
                    k = 10,
                    )
            # if best_hit < hit:
            #     best_hit = hit
            #     torch.save(model.state_dict(), os.path.join(args.model_path, args.model_name))
            tbar.set_description(f'Epoch: {epoch:3d}| Train loss: {train_loss:.5f}| NDCG@10: {ndcg:.5f}| HIT@10: {hit:.5f}')

if __name__ == "__main__":
    args = parse_args()
    main(args)
