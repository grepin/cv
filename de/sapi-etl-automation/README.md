# ETL: миграции, идемпотентность
1. ETL-автоматизация через Airflow [DAG](/de/sapi-etl-automation/src/dags/dag.py)
1. Миграции включены в код DAG-а в качестве PostgresqlOperator, равно как и очистка таблиц, код представлен [SQL-файлом](de/sapi-etl-automation/src/dags/sql/migrations.sql) в общей папке SQL
1. Идемпотентность - через поле updated_at по [execution time DAG run-а](/de/sapi-etl-automation/src/dags/dag.py#L106) в staging.user_order_log - она же для mart.f_sales как обновление из соответствующего order_log
1. Для mart.f_customer_retention - полное пересоздание; в ней updated_at играет лишь роль "индикатора даты данных для недели"

