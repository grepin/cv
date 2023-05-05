from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_data_with_depth, distance
from pyspark.sql.window import Window
import sys
import pyspark.sql.functions as F


date = sys.argv[1]
depth = int(sys.argv[2])
mode = sys.argv[3]

assert date is not None
assert depth is not None
assert mode is not None
assert mode in ('overwrite', 'append')


spark = spark_session(app="data_events")
raw = read_data_with_depth(spark, date, depth, path=Paths.EVENTS_RAW_PATH)
cities = spark.read.parquet(Paths.DATA_CITIES_PATH)

window = Window().partitionBy('message_id')
raw\
    .select('event.message_id', 'lat', 'lon') \
    .crossJoin(cities) \
    .withColumn('distance', distance(F.col('city_lat'), F.col('city_lon'), F.col('lat'), F.col('lon'))) \
    .select('message_id', 'city', 'timezone', 'distance') \
    .withColumn('min_distance', F.min('distance').over(window))\
    .where("distance == min_distance")\
    .select('message_id', 'city', 'timezone') \
    .join(
        raw.select('event', 'event_type', 'date', 'lat', 'lon'),
        F.col('event.message_id') == F.col('message_id'), how='inner') \
    .select('event', 'event_type', 'date', 'city', 'timezone', 'lat', 'lon')\
    .write.partitionBy('date').mode(mode).parquet(Paths.DATA_EVENTS_PATH)
