import lib.env
from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 6, 18),
    'end_date': datetime(2022, 6, 21)
}

dag_spark = DAG(
    dag_id="spark_etl_dag",
    default_args=default_args,
    schedule_interval='@daily',
    catchup=True,
)


def sso(task_id: str, app: str, args: list) -> SparkSubmitOperator:
    return SparkSubmitOperator(
        task_id=task_id,
        dag=dag_spark,
        application=app,
        conn_id='yarn',
        application_args=args,
        executor_cores=2,
        executor_memory='8g'
    )


events = sso(task_id='data_events', app='/lessons/dags/data_events.py', args=["{{ ds }}", "1", "overwrite"])
user = sso(task_id='mart_user', app='/lessons/dags/mart_user.py', args=["{{ ds }}", "90", "27"])
geo = sso(task_id='mart_geo', app='/lessons/dags/mart_geo.py', args=["{{ ds }}"])
friends = sso(task_id='mart_friends', app='/lessons/dags/mart_friends.py', args=["{{ ds }}"])

events >> user >> geo >> friends
