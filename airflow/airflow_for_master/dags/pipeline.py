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

    #Task Using docker for SASREC training 
    #.. 깃허브는 public으로 변할꺼니까.. 지금은 프라이빗이고.. 코드자체를 공개할수는 없는데 .. 도커이미지를 도커허브에 올릴수도 없고... - docker load를 이용하자?
    sasrec_training_docker = DockerOperator(
        image= '',
        docker_url='unix://var/run/docker.sock',
        command = '',
        network_mode = 'bridge',
        auto_remove = 'force',
        device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],
        )
    
    #Fast_Api_start_task-TFIDF
    


    #Task 5 Using slack noti - for training_end

    # DAG 간의 의존성 설정
    # 다른 작업들과의 의존성이 있다면 여기에 추가i
    slack_noti >> bash_for_start >> do >> bash_task2

    # DAG 실행q

