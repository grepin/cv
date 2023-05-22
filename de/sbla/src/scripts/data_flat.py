from lib.session import spark_session
from lib.variables import Paths
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, MapType
import pyspark.sql.functions as F
import sys

processed = sys.argv[1]
file = sys.argv[2]
mode = sys.argv[3]
par = 1


def flatten(jdf, prefix=""):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("path", StringType(), True),
        StructField("value", StringType(), True),
        StructField("type", StringType(), True),
    ])
    udf = spark.createDataFrame(schema=schema, data=[])
    id = 'identifier'
    sep = '=>'

    def recursion(df, prefix=""):
        nonlocal udf
        for column in df.columns:
            dtype = df.select(column).schema[0].dataType
            if isinstance(dtype, StructType):
                sdf = df.select(id, column + ".*").repartition(par, id)
                recursion(sdf, prefix=prefix + sep + column)
            elif isinstance(dtype, ArrayType):
                adf = df\
                    .select(id, F.posexplode(column))\
                    .groupBy(id).pivot("pos")\
                    .agg(F.first(F.col('col')))\
                    .repartition(par, id)
                recursion(adf, prefix=prefix + sep + column)
            elif isinstance(dtype, MapType):
                mdf = df\
                    .select(id, F.explode(column))\
                    .groupBy(id).pivot("key")\
                    .agg(F.first(F.col('value')))\
                    .repartition(par, id)
                recursion(mdf, prefix=prefix + sep + column)
            else:
                cdf = df\
                    .select(id, F.col(column).cast(StringType()).alias('value'))\
                    .withColumn('path', F.lit(prefix + sep + column))\
                    .withColumn('type', F.lit(str(dtype)))\
                    .select(id, 'path', 'value', 'type')\
                    .repartition(par, id)
                udf = udf.union(cdf)

    recursion(jdf, prefix=prefix)
    nmr = udf.repartition(par, 'id').where(~F.col('path').endswith(sep + id))
    modified = nmr\
        .where(F.col('path').endswith("root" + sep + "modified"))\
        .select(F.col('id').alias('mid'), F.col('value').alias('modified'))\
        .repartition(1, 'mid')\
        .distinct()\
        .hint('broadcast')
    return nmr\
        .join(modified, F.col('id') == F.col('mid'), how='left')\
        .select('id', 'modified', 'path', 'value', 'type')


spark = spark_session(master="local[*]", app="raw")
df = spark\
    .read\
    .json(Paths.JSON_PATH + file)\
    .cache()

df\
    .repartition(1)\
    .write\
    .parquet(Paths.RAW_PATH + '/uploaded=' + processed, mode=mode)

pdf = df\
    .select(F.explode('dataset').alias('ds'))\
    .select('ds.*')\
    .repartition(par)

flat = flatten(pdf, prefix="root")
flat\
    .repartition(1)\
    .write \
    .parquet(Paths.FLAT_PATH + '/processed=' + processed, mode=mode)


