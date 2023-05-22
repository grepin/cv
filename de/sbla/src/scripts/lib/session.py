import lib.env
from pyspark.sql import SparkSession


def spark_session(master: str = "yarn", app: str = "app") -> SparkSession:
    return SparkSession \
        .builder \
        .master(master) \
        .appName(app) \
        .config("spark.dynamicAllocation.enabled", "true")\
        .config("spark.dynamicAllocation.minExecutors", "1")\
        .config("spark.dynamicAllocation.maxExecutors", "10")\
        .config("spark.executor.cores", "4")\
        .config("spark.sql.files.ignoreMissingFiles", "true") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760") \
        .config("spark.driver.memory", "8g") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
