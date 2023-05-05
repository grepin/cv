from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_data_with_depth
from pyspark.sql.window import Window
import sys
import pyspark.sql.functions as F


date = sys.argv[1]
depth = int(sys.argv[2])
home_seq_days = int(sys.argv[3])

assert date is not None
assert depth is not None
assert home_seq_days is not None


spark = spark_session(app="mart_user")
events = read_data_with_depth(spark, date, depth, path=Paths.DATA_EVENTS_PATH)

transfer_base = events \
    .where('event.message_from is not null') \
    .select(
        'event.message_from',
        'city',
        F.coalesce(
            F.col('event.message_ts'),
            F.col('event.datetime'),
            F.to_timestamp('date', 'yyyy-MM-dd')
        ).alias('date'))\
    .distinct()\
    .cache()

transfer_index_date = Window.partitionBy('message_from').orderBy(F.col('date').desc())
transfer_index_date_city = Window.partitionBy('message_from', 'city').orderBy(F.col('date').desc())

transfer = transfer_base\
    .withColumn('index_date', F.row_number().over(transfer_index_date)) \
    .withColumn('index_date_city', F.row_number().over(transfer_index_date_city)) \
    .withColumn('seq', F.col('index_date') - F.col('index_date_city')) \
    .groupBy('message_from', 'city', 'seq')\
    .agg(F.min('date').alias('date'), F.max('date').alias('end_date'))\
    .withColumn('delta', F.datediff(F.col('end_date'), F.col('date')))\
    .select('message_from', 'city', 'date', 'end_date', 'delta')

home_window = Window()\
    .partitionBy('message_from')\
    .orderBy(F.col('delta').desc())

home = transfer\
    .where('delta >= {0}'.format(home_seq_days)) \
    .withColumn('rn', F.row_number().over(home_window)) \
    .where('rn == 1')\
    .select('message_from', 'city')

travel_cities_window = Window() \
    .partitionBy('message_from') \
    .orderBy(F.col('date').asc()) \
    .rangeBetween(Window.unboundedPreceding, Window.unboundedFollowing)

travel_cities = transfer\
    .select('message_from', 'city', 'date') \
    .withColumn('travel_count', F.count("*").over(travel_cities_window)) \
    .withColumn('travel_array', F.collect_list('city').over(travel_cities_window)) \
    .select('message_from', 'travel_count', 'travel_array') \
    .distinct()

home_fallback_window = Window()\
    .partitionBy('message_from')\
    .orderBy(F.col('count').desc())\
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

home_fallback = events\
    .where('event.message_from is not null') \
    .select('event.message_from', 'city') \
    .groupBy('message_from', 'city') \
    .agg(F.count('city').alias('count')) \
    .withColumn('r', F.row_number().over(home_fallback_window)) \
    .where('r == 1') \
    .select('message_from', 'city') \
    .distinct()


last_message_city_window = Window() \
    .partitionBy('message_from') \
    .orderBy(F.col('datetime').desc()) \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

last_message_city = events\
    .where("event.message_from is not null") \
    .select(
        'event.message_from',
        'city',
        'date',
        F.coalesce(
            F.col('event.datetime'),
            F.col('event.message_ts'),
            F.to_timestamp('date', 'yyyy-MM-dd')
        ).alias('datetime'),
        'timezone',
        'lat',
        'lon') \
    .withColumn('r', F.row_number().over(last_message_city_window)) \
    .where('r == 1') \
    .select('message_from', 'city', 'timezone', 'datetime', 'lat', 'lon') \
    .distinct()

events\
    .where('event.message_from is not null') \
    .select(F.col('event.message_from').alias('mf')) \
    .distinct() \
    .join(
        last_message_city.select(F.col('message_from').alias('lcmf'), F.col('city').alias('lc'), 'datetime', 'lat', 'lon', 'timezone'),
        F.col('mf') == F.col('lcmf'),
        how='left') \
    .join(
        home.select(F.col('message_from').alias('hmf'), F.col('city').alias('hc')),
        F.col('mf') == F.col('hmf'),
        how='left') \
    .join(
        home_fallback.select(F.col('message_from').alias('hfmf'), F.col('city').alias('hfc')),
        F.col('mf') == F.col('hfmf'),
        how='left')\
    .join(
        travel_cities.select(F.col('message_from').alias('tcmf'), 'travel_count', 'travel_array'),
        F.col('mf') == F.col('tcmf'),
        how='left') \
    .select(
        F.col('mf').alias('user_id'),
        F.col('lc').alias('act_city'),
        F.from_utc_timestamp(
            F.col('datetime'),
            F.col('timezone')
        ).alias('local_time'),
        F.col('lat').alias('act_lat'),
        F.col('lon').alias('act_lon'),
        F.coalesce('hc', 'hfc').alias('home_city'),
        F.col('travel_count'),
        F.col('travel_array'),
    ).write.mode('overwrite').parquet(Paths.MART_USER_PATH + '/processed_dttm=' + date)
