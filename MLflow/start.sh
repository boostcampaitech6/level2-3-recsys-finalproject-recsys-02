#!/bin/sh
mlflow server --host 0.0.0.0 --backend-store-uri postgresql://postgres:recsys021234@10.0.1.7:5432/mldb --default-artifact-root s3://mlflow/
