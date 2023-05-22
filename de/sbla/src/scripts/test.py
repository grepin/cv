from lib.session import spark_session
from lib.variables import Paths
from lib.utils import read_partial
import sys
import pyspark.sql.functions as F
from pyspark.sql.window import Window

date_curr = sys.argv[1]
date_prev = sys.argv[2]
par = 1

spark = spark_session(master="local[*]", app="raw")
df_prev = read_partial(spark, Paths.FLAT_PATH + '/processed=' + date_prev, par).cache()
df_curr = read_partial(spark, Paths.FLAT_PATH + '/processed=' + date_curr, par).cache()
df_diff = read_partial(spark, Paths.DIFF_PATH + '/processed=' + date_curr, par).cache()

new_ones = df_curr\
    .select('id')\
    .distinct()\
    .join(df_prev.select('id').distinct(), df_curr.id == df_prev.id, how='left_anti')\
    .sort('id')\
    .cache()

assert new_ones.count() == 10
print("List of new documents")
new_ones.show(10, truncate=False)

modified_paths = df_diff.sort('jws')
assert modified_paths.count() == 70
print("List of modified attributes")
modified_paths.show(70, truncate=False)

modified_docs = df_diff\
    .select('id')\
    .distinct()
assert modified_docs.count() == 10
print("List of modified documents")
modified_docs.show(10, truncate=False)

window = Window.partitionBy('id').orderBy('jws')
df_diff_top5 = df_diff\
    .withColumn('rn', F.row_number().over(window))\
    .where('rn <= 5')
assert df_diff_top5.count() == 50
print("List of Top-5 modified columns for modified documents")
df_diff_top5.select('id', 'rn', 'modified', 'path', 'jws', 'value', 'value_prev').show(50, truncate=False)


