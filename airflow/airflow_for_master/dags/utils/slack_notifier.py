from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.operators.empty import EmptyOperator

# Slack Webhook 제공 Operator 를 먼저 정의합니다
# 1. Connection ID (실습에서 Webserver 를 통해 생성한 값)
SLACK_DAG_CONN_ID = "my_webhook"


# 2. Webhook 함수 정의
def send_message(slack_msg):
    return SlackWebhookOperator(
        task_id="slack_webhook",
        slack_webhook_conn_id=SLACK_DAG_CONN_ID,
        message=slack_msg,
        username="Airflow-alert",
    )
def call_empthy():
    return EmptyOperator(task_id="end")


# 3. slack alert 함수 정의
# 메시지에 Slack ID 추가해 tag 가능 (ex. <@U022T50D4F5>)
def task_fail_slack_alert(context):
    slack_msg = """
            :red_circle: Task Failed.
            *Task*: {task}  
            *Dag*: `{dag}` 
            *Execution Time*: {exec_date}
            """.format(
        task=context.get("task_instance").task_id,
        dag=context.get("task_instance").dag_id,
        exec_date=context.get("execution_date"),
    )

    alert = send_message(slack_msg)

    return alert.execute(context=context)

