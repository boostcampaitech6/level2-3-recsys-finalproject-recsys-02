FROM python:3.9-slim

ENV TZ Asia/Seoul

WORKDIR /app

COPY . .

EXPOSE 8000

RUN apt-get update && apt-get upgrade -y && \
    pip install -U pip &&\
    pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
