FROM amd64/python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip &&\
    pip install mlflow==1.30.0 psycopg2-binary

ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]