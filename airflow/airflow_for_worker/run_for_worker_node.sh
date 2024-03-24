#! /bin/sh


distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
docker build -t airflow_worker:1.0 .
docker run -d -it --restart=always --name worker1 -p 8080:8080 \
-v ~/airflow_worker/dags:/root/airflow/dags \
-v ~/airflow_worker/plugins:/root/airflow/plugins \
-v ~/airflow_worker/log:/root/airflow/log \
-v /etc/localtime:/etc/localtime:ro -e TZ=Asia/Seoul \
airflow_worker:1.0 \
airflow celery worker -H worker1 -q queue1
