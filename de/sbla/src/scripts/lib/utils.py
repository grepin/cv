from pyspark.sql import DataFrame, SparkSession


def read_partial(session: SparkSession, path: str, partitions) -> DataFrame:
    return session\
        .read\
        .option("basePath", path)\
        .parquet(path)\
        .repartition(partitions)
