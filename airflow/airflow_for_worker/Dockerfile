#for worker nodes

FROM ubuntu:latest

# install airflow
ENV AIRFLOW_HOME="/root/airflow"
ENV AIRFLOW__WORKER__NAME="worker_node"

ENV AIRFLOW__MASTER__IP="10.0.1.6"
ENV AIRFLOW__POSTGRESQL__HOST=${AIRFLOW__MASTER__IP}:5432
ENV AIRFLOW__REDIS__HOST=${AIRFLOW__MASTER__IP}:6379
ENV AIRFLOW__CORE__EXECUTOR="CeleryExecutor"
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://airflow:airflow@${AIRFLOW__POSTGRESQL__HOST}/airflow"
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://airflow:airflow@${AIRFLOW__POSTGRESQL__HOST}/airflow"
ENV AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://airflow:airflow@${AIRFLOW__POSTGRESQL__HOST}/airflow"
ENV AIRFLOW__CELERY__BROKER_URL="redis://:@${AIRFLOW__REDIS__HOST}/0"
ENV AIRFLOW__LOGGING__BASE_LOG_FOLDER="${AIRFLOW_HOME}/log"
ENV AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY="${AIRFLOW_HOME}/log/scheduler"
ENV AIRFLOW__LOGGING__DAG_PROCESSOR_MANAGER_LOG_LOCATION="${AIRFLOW_HOME}/log/dag_processor_manager/dag_processor_manager.log"
ENV AIRFLOW__CORE__HOSTNAME_CALLABLE="airflow.utils.net.get_host_ip_address"
ENV AIRFLOW__CORE__FERNET_KEY="3IAaJLLoinZznxT_D5uyeJwlUqmh6afqNcqTkVsoLwQ="
ENV AIRFLOW__WEBSERVER__SECRET_KEY="b'c!~c=4\xd25\x19\x07IG\xb02+\x82'"
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION="true"
ENV AIRFLOW__CORE__LOAD_EXAMPLES="false"
ENV AIRFLOW__API__AUTH_BACKENDS="airflow.api.auth.backend.basic_auth"
ENV _PIP_ADDITIONAL_REQUIREMENTS="${_PIP_ADDITIONAL_REQUIREMENTS:-apache-airflow-providers-google}"

RUN set -xe \
    && apt-get -y update \
    && apt-get -y install python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install apache-airflow[celery]==2.8.3
RUN pip3 install psycopg2-binary
RUN pip3 install Redis
RUN airflow db init
RUN mkdir -p /root/airflow/dags
RUN mkdir -p /root/airflow/plugins

RUN mkdir -p /etc/moreh
RUN echo ${SDA_TOKEN} > /etc/moreh/token

RUN apt-get update
RUN apt-get -y install lsb-release apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN apt-get -y upgrade apt-transport-https
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey
RUN apt-key add /tmp/dkey
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get -y install docker-ce docker-ce-cli containerd.io
RUN pip3 install apache-airflow-providers-docker

CMD ["/bin/bash"]
