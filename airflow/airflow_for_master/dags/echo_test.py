from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

# DAG 정의
dag = DAG(
    'docker_test',
    description='Example DAG with BashOperator',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Bash 스크립트 정의
bash_script = """
echo "Hello, Airflow!"
echo "Current date: $(date)"
"""

# BashOperator 정의
bash_task = BashOperator(
    task_id='bash_task',
    bash_command=bash_script,
    dag=dag,
)

do = DockerOperator(
       task_id='docker_sample_task',
       image='myhome.hahaha.com/hadoop-client:latest',
       command="echo temp; sleep 10 ; echo temp",
       api_version='auto',
       auto_remove=True,
       docker_url="unix://var/run/docker.sock",
       network_mode="bridge"
    )

bash_task2 = BashOperator(
    task_id='bash_task2',
    bash_command=bash_script,
    dag=dag,
)

# DAG 간의 의존성 설정
# 다른 작업들과의 의존성이 있다면 여기에 추가i
bash_task >> do >> bash_task2

# DAG 실행
