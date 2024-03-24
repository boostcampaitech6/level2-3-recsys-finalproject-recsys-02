from args import parse_args
from dataloader import data_load
from model import SASRec
from trainer import train, evaluate
import torch
import datetime
import os
import mlflow
import mlflow.sklearn

def main(args):

    print(f'----------------------Load Data----------------------')
    user_train, user_valid, num_item, num_user, num_batch = data_load(args)

    print(f'----------------------Load Model----------------------')
    args.device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SASRec(num_user, num_item, args.hidden_units, args.num_heads,
                   args.num_layers, args.max_len, args.dropout_rate, args.device)
    model.to(args.device)
    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    print(f'----------------------Training----------------------')
    os.environ["MLFLOW_TRACKING_URI"] = "SECRET"
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "SECRET"
    os.environ["AWS_ACCESS_KEY_ID"] = "SECRET"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "SECRET"
    
    # 마스터노드로 모델 아티팩트 복사
    experiment_name = "SASRec_experiment"

    # 처음 실행시
    #mlflow.create_experiment(experiment_name, artifact_location="s3://mlflow/")

    #mlflow.get_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:
        artifact_uri = run.info.artifact_uri
        print(artifact_uri)
        train(model, optimizer, criterion, args.num_epochs, num_batch,
            user_train, num_user, num_item, args.batch_size, args.max_len, args.device)
        
        # Log the model to MLflow
        mlflow.pytorch.log_model(model, "model")
    
        print(f'----------------------Evaluate----------------------')
        evaluate(model, num_user, user_train, user_valid, num_item, args)

        mlflow.end_run()

if __name__ == "__main__":
    args = parse_args()
    main(args)
