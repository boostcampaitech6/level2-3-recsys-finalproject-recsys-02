FROM amd64/python:3.9-slim

WORKDIR /usr/app

RUN pip install -U pip &&\
    pip install "fastapi[all]"

COPY main.py main.py

CMD ["uvicorn", "main.py", "--host", "0.0.0.0", "--reload"]
