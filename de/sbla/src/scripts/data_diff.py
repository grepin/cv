from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_partial
import sys
import ceja
import pyspark.sql.functions as F

date_curr = sys.argv[1]
date_prev = sys.argv[2]
mode = sys.argv[3]
par = 1

spark = spark_session(master="local[*]", app="raw")
df_prev = read_partial(spark, Paths.FLAT_PATH + '/processed=' + date_prev, par).cache()
df_curr = read_partial(spark, Paths.FLAT_PATH + '/processed=' + date_curr, par).cache()

diff = df_curr\
    .join(
        df_prev,
        (
            (df_curr.id == df_prev.id) &
            (df_curr.path == df_prev.path) &
            (F.coalesce(df_curr.value, F.lit('')) != F.coalesce(df_prev.value, F.lit('')))
        ),
        how='inner')\
    .select(
        df_curr.id,
        df_curr.modified,
        df_curr.path,
        df_curr.value,
        df_prev.value.alias('value_prev')
    ).withColumn('jws',
        ceja.jaro_winkler_similarity(
            F.coalesce(F.col("value"), F.lit('')),
            F.coalesce(F.col("value_prev"), F.lit(''))
        )
    )\
    .select('id', 'modified', 'path', 'jws', 'value', 'value_prev')

diff\
    .repartition(1)\
    .write\
    .parquet(Paths.DIFF_PATH + '/processed=' + date_curr, mode=mode)
