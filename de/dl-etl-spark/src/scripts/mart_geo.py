from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_data_with_depth
import sys
import pyspark.sql.functions as F
from datetime import datetime

date = sys.argv[1]

assert date is not None

depth = (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(date[:-3], "%Y-%m")).days

spark = spark_session(app="mart_geo")
wdf = read_data_with_depth(spark, date, depth, path=Paths.DATA_EVENTS_PATH)\
    .withColumn('month', F.date_trunc('month', F.col('date'))) \
    .withColumn('week', F.date_trunc('week', F.col('date'))) \
    .groupBy('city', 'month', 'week') \
    .agg(
        F.count(F.when(F.col('event_type') == 'message', True)).alias('week_message'),
        F.count(F.when(F.col('event_type') == 'reaction', True)).alias('week_reaction'),
        F.count(F.when(F.col('event.subscription_user').isNotNull(), True)).alias('week_subscription'),
        F.countDistinct(F.when(F.col('event.message_from').isNotNull(), True)).alias('week_user')
    )
mdf = wdf\
    .groupBy('city', 'month')\
    .agg(
        F.sum('week_message').alias('month_message'),
        F.sum('week_reaction').alias('month_reaction'),
        F.sum('week_subscription').alias('month_subscription'),
        F.sum('week_user').alias('month_user')
    ).select(
        F.col('city').alias('month_city'),
        F.col('month').alias('month_month'),
        F.col('month_message'),
        F.col('month_reaction'),
        F.col('month_message'),
        F.col('month_subscription'),
        F.col('month_user')
    )
df = mdf\
    .join(wdf, (F.col('month_city') == F.col("city")) & (F.col('month_month') == F.col("month")), how='inner')\
    .select(
        'city',
        'month',
        'week',
        'month_message',
        'month_reaction',
        'month_message',
        'month_subscription',
        'month_user',
        'week_message',
        'week_reaction',
        'week_subscription',
        'week_user'
    ).write.mode('overwrite').parquet(Paths.MART_GEO_PATH + '/processed_dttm=' + date)

