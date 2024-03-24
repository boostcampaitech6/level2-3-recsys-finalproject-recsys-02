from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# DAG 정의
dag = DAG(
    'bash_operator_example',
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

# DAG 간의 의존성 설정
# 다른 작업들과의 의존성이 있다면 여기에 추가i
bash_task

# DAG 실행
