import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda", type=str, help="cpu or gpu")

    # TM args
    parser.add_argument("--num_topics", default=24, type=int, help="number of topics")
    parser.add_argument("--random_state", default=42, type=int, help="LDAmodel_random_state")
    parser.add_argument("--passes", default=20, type=int, help="LDAmodel_passes")
    
    # model
    parser.add_argument("--emb_dim", default=24, type=int, help="hidden dimension size")
    parser.add_argument("--reg", default=1e-5, type=int, help="regularization")
    parser.add_argument("--n_layers", default=2, type=int, help="number of layers")
    parser.add_argument("--node_dropout", default=0.2, type=float, help="drop out rate")
    parser.add_argument("--valid_samples", default=2, type=int, help="valid samples")

    # train
    parser.add_argument("--seed", default=22, type=int, help="seed")
    parser.add_argument("--num_epochs", default=150, type=int, help="number of epochs")
    parser.add_argument("--batch_size", default=64, type=int, help="batch size")
    parser.add_argument("--lr", default=0.0001, type=float, help="learning rate")
    parser.add_argument("--n_batch", default=10, type=int, help="n_batch")

    args = parser.parse_args()

    return args
