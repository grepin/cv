from lib.session import spark_session
from lib.variables import Paths

spark = spark_session(app="data_cities")
spark\
    .read\
    .option("delimiter", ";") \
    .option("header", "true") \
    .csv(Paths.CITIES_CSV_PATH) \
    .selectExpr(
        "cast(id as int) id",
        "city",
        "timezone",
        "cast(replace(lat,',','.') as double) city_lat",
        "cast(replace(lng,',','.') as double) city_lon") \
    .write \
    .mode('overwrite') \
    .parquet(Paths.DATA_CITIES_PATH)
