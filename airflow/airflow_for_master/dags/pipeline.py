from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.operators.empty import EmptyOperator

from utils.slack_notifier import task_succ_slack_alert, task_fail_slack_alert
SLACK_DAG_CONN_ID = "slack_noti"
# DAG 정의
with DAG(
    'PipeLine',
    description='Whole PipeLine for Training',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 3, 27),
    catchup=False,
    on_failure_callback=task_fail_slack_alert,
    on_success_callback=task_succ_slack_alert
) as dag:
    #Notifiying task start for users by slack message
    slack_noti = SlackWebhookOperator(
            task_id="slack_noti",
            slack_webhook_conn_id = "slack_noti",
            message=""":
                    task_start
                    """,
            username="airflow"
    )

    #Start_noti_bash
    starting_bash_string = """
    echo "Hello, Airflow!"
    echo "Current date: $(date)"
    """
    bash_for_start = BashOperator(
        task_id='Start_noti_bash',
        bash_command=starting_bash_string,
        dag=dag,
    ) 

    #Task 1 Using docker - Fast_Api_start_task-TFIDF
    do = DockerOperator(
        )


    #Task 5 Using slack noti - for training_end

    # DAG 간의 의존성 설정
    # 다른 작업들과의 의존성이 있다면 여기에 추가i
    slack_noti >> bash_for_start >> do >> bash_task2

    # DAG 실행q

