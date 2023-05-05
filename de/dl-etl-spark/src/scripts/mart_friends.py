from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_data_with_depth, distance
import sys
import pyspark.sql.functions as F


date = sys.argv[1]
depth = int(sys.argv[2])

assert date is not None
assert depth is not None

spark = spark_session(app="mart_friends")
events = spark.read.parquet(Paths.DATA_EVENTS_PATH)

user_channels = events.where(F.col('event.channel_id').isNotNull())\
    .select(F.col('event.message_from').alias('user'), F.col('event.channel_id').alias('channel'))\
    .distinct()

have_common_channel_pairs = user_channels\
    .select(F.col('user').alias('uc1'), F.col('channel').alias('c1'))\
    .crossJoin(user_channels.select(F.col('user').alias('uc2'), F.col('channel').alias('c2')))\
    .where((F.col('uc1') < F.col('uc2')) & (F.col('c1') == F.col('c2')))\
    .select(F.concat(F.least('uc1', 'uc2'), F.lit('-'), F.greatest('uc1', 'uc2')).alias('common_channel'))\
    .distinct()


have_common_message_pairs = events\
    .where(F.col('event.message_to').isNotNull() & (F.col('event_type') == 'message'))\
    .select(F.col('event.message_from').alias('from'), F.col('event.message_to').alias('to'))\
    .select(F.concat(F.least('from', 'to'), F.lit('-'), F.greatest('from', 'to')).alias('common_message'))\
    .distinct()

have_common_channel_and_no_common_message = have_common_channel_pairs\
    .join(
        have_common_message_pairs,
        F.col('common_message') == F.col('common_channel'),
        how='left_anti')\
    .withColumn('user_left', F.split(F.col('common_channel'), '-').getItem(0)) \
    .withColumn('user_right', F.split(F.col('common_channel'), '-').getItem(1)) \
    .select('user_left', 'user_right')

user_mart = spark.read.parquet(Paths.MART_USER_PATH + '/processed_dttm=' + date)\
    .select('user_id', 'act_city', 'act_lat', 'act_lon', 'local_time')

propose_friendship = have_common_channel_and_no_common_message\
    .join(user_mart.select(
            F.col('user_id').alias('user_id_left'),
            F.col('act_lat').alias('lat_left'),
            F.col('act_lon').alias('lon_left'),
            F.col('act_city').alias('city_left'),
            F.col('local_time').alias('local_time_left')
        ), F.col('user_left') == F.col('user_id_left'), how='inner') \
    .join(user_mart.select(
            F.col('user_id').alias('user_id_right'),
            F.col('act_lat').alias('lat_right'),
            F.col('act_lon').alias('lon_right'),
            F.col('act_city').alias('city_right'),
            F.col('local_time').alias('local_time_right')
        ), F.col('user_right') == F.col('user_id_right'), how='inner') \
    .withColumn('distance', distance(F.col('lat_left'), F.col('lon_left'), F.col('lat_right'), F.col('lon_right')))\
    .where('distance <= 1') \
    .select(
        'user_left',
        'user_right',
        F.coalesce(F.col('local_time_left'), F.col('local_time_right')).alias('local_time'),
        'city_left',
        'city_right'
    )\
    .write.mode('overwrite').parquet(Paths.MART_FRIENDS_PATH + '/processed_dttm=' + date)
