FROM amd64/python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip &&\
    pip install mlflow==1.30.0 psycopg2-binary boto3

ADD start.sh /
RUN chmod +x /start.sh
ENV AWS_ACCESS_KEY_ID admin
ENV AWS_SECRET_ACCESS_KEY changeme
ENV MLFLOW_S3_ENDPOINT_URL http://10.0.1.6:9000
CMD ["/start.sh"]
