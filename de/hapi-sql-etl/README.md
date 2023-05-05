# Инкрементальная послойная укладка, SQL + API, с ETL-автоматизацией через Airflow
* Общая логика слоев - в [api_entities.md](/de/hapi-sql-etl/api_entities.md)
* [ETL-wrapper](/de/hapi-sql-etl/src/dags/lib/etl_wrapper.py) унифицирован под разные виды загрузок с курсором
* Для каждого слоя - отдельный DAG с соответствующим именем
* Работа с асинхронностью загрузки между stg и dds - через "сквозное" использование autoincrement-идентификаторов из stg в dds и использование возвращаемых значений  
* [Итоговая витрина](/de/hapi-sql-etl/src/dags/mart/00.cdm.dm_courier_legder.sql) - классический [execution-date-based-DAG-wrapper](/de/hapi-sql-etl/src/dags/cdm.py#L18), перезписывающий данные за месяц 
