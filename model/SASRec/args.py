import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu", type=str, help="cpu or gpu")

    parser.add_argument(
        "--max_len", default=10, type=int, help="max sequence length"
    ) 
    parser.add_argument("--num_workers", default=1, type=int, help="number of workers") 

    # 모델
    parser.add_argument(
        "--hidden_units", default=50, type=int, help="hidden dimension size"
    ) 
    parser.add_argument("--num_layers", default=2, type=int, help="number of layers") 
    parser.add_argument("--num_heads", default=1, type=int, help="number of heads") 
    parser.add_argument("--dropout_rate", default=0.5, type=float, help="drop out rate") 

    # 훈련
    parser.add_argument("--num_epochs", default=50, type=int, help="number of epochs") 
    parser.add_argument("--batch_size", default=128, type=int, help="batch size") 
    parser.add_argument("--lr", default=0.001, type=float, help="learning rate") 

    args = parser.parse_args()

    return args