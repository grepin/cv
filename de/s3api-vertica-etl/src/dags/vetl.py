import vertica_python
from airflow.decorators import dag
import pendulum
from airflow.operators.python import PythonOperator
import os
from pathlib import Path
import boto3
from airflow.sensors.base_sensor_operator import BaseSensorOperator

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

conn_info = {
    'host': os.getenv('VERTICA_HOST'),
    'port': os.getenv('VERTICA_PORT'),
    'user': os.getenv('VERTICA_USER'),
    'password': os.getenv('VERTICA_PASSWORD'),
    'database': os.getenv('VERTICA_DATABASE'),
    'autocommit': True
}

stg_specs = {
    'users': {
        'schema': 'GEORGYVREPINYANDEXRU__STAGING',
        'tablename': 'users',
        'fields_spec': '(id, chat_name, registration_dt, country, age)',
        'filepath': '/data/users.csv',
    },
    'groups': {
        'schema': 'GEORGYVREPINYANDEXRU__STAGING',
        'tablename': 'groups',
        'fields_spec': '(id, admin_id, group_name, registration_dt, is_private)',
        'filepath': '/data/groups.csv',
    },
    'dialogs': {
        'schema': 'GEORGYVREPINYANDEXRU__STAGING',
        'tablename': 'dialogs',
        'fields_spec': '(message_id, message_ts, message_from, message_to, message, message_group)',
        'filepath': '/data/dialogs.csv',
    },
    'group_log': {
        'schema': 'GEORGYVREPINYANDEXRU__STAGING',
        'tablename': 'group_log',
        'fields_spec': '(group_id, user_id, user_id_from, event, datetime)',
        'filepath': '/data/group_log.csv',
    }
}


class MultipleFileSensor(BaseSensorOperator):
    def __init__(self, filepaths, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepaths = filepaths

    def poke(self, context):
        for file in self.filepaths:
            if not os.path.exists(file):
                return False
        return True


def fetch_s3_file(bucket: str, key: str):
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3_client.download_file(
        Bucket=bucket,
        Key=key,
        Filename='/data/{0}'.format(key)
    )


def vertica_execute(sql_file: str):
    with vertica_python.connect(**conn_info) as conn:
        curs = conn.cursor()
        curs.execute(Path(sql_file).read_text())


def vertica_copy(schema: str, tablename: str, fields_spec: str, filepath: str):
    with vertica_python.connect(**conn_info) as conn:
        curs = conn.cursor()
        curs.execute(f"TRUNCATE TABLE {schema}.{tablename}")
        curs.execute(
            """
            COPY {0}.{1}{2}
            FROM LOCAL '{3}'
            DELIMITER ','
            SKIP 1
            REJECTED DATA AS TABLE {0}.{1}_rej; 
            """.format(schema, tablename, fields_spec, filepath)
        )


@dag(schedule_interval=None, start_date=pendulum.parse('2022-07-13'))
def vetl():
    sql_dir = '/lessons/dags/sql/'
    schema_tasks = []
    for ddl in sorted([file for file in os.listdir(sql_dir) if file.startswith('ddl')]):
        schema_tasks.append(
            PythonOperator(
                task_id='sch_{0}'.format(ddl.split('.')[3]),
                python_callable=vertica_execute,
                op_kwargs={'sql_file': sql_dir + ddl},
            )
        )

    bucket_files = ['users.csv', 'groups.csv', 'dialogs.csv', 'group_log.csv']
    fetch_tasks = []
    for file in bucket_files:
        fetch_tasks.append(
            PythonOperator(
                task_id='fetch_{0}'.format(file),
                python_callable=fetch_s3_file,
                op_kwargs={'bucket': 'sprint6', 'key': file},
            )
        )

    stg_tasks = []
    for name in stg_specs:
        stg_tasks.append(
            PythonOperator(
                task_id='load_{0}'.format(name),
                python_callable=vertica_copy,
                op_kwargs=stg_specs[name],
            )
        )

    insert_tasks = []
    for dml in sorted([file for file in os.listdir(sql_dir) if file.startswith('dml')]):
        insert_tasks.append(
            PythonOperator(
                task_id='ins_{0}'.format(dml.split('.')[4]),
                python_callable=vertica_execute,
                op_kwargs={'sql_file': sql_dir + dml},
            )
        )

    files_sensor = MultipleFileSensor(task_id='fetched', filepaths=['/data/' + file for file in bucket_files])
    for i in range(len(schema_tasks) - 1):
        schema_tasks[i] >> schema_tasks[i+1]
    schema_tasks[i+1] >> fetch_tasks >> files_sensor >> stg_tasks >> insert_tasks[0]
    for i in range(len(insert_tasks) - 1):
        insert_tasks[i] >> insert_tasks[i+1]


dag = vetl()
