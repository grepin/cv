
# Vertica + API, ETL с Airflow-автоматизацией (+ручные выборки)
* Вся работа - в рамках DAG [vetl.py](/de/s3api-vertica-etl/src/dags/vetl.py). One-shot run, исходя из общей постановки
* Все DDL/DML в подпапке [/src/dags/sql](/de/s3api-vertica-etl/src/dags/sql)
* CTE по ответам на вопросы бизнеса - в [/src/sql](/de/s3api-vertica-etl/src/sql) - их запуск вне DAG-а, как итоговая аналитика
* .env.sample - с названиями переменных, которые необходимо определить для корректного запуска

