import datetime
from lib.variables import Paths
import pyspark.sql.functions as F


def input_paths(date: str, depth: int, extended_partitions: str = "", path: str = Paths.DATA_EVENTS_PATH):
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    return [f"{path}/date={(dt-datetime.timedelta(days=x)).strftime('%Y-%m-%d')}/{extended_partitions}" for x in range(depth)]


def read_data_with_depth(
        spark,
        date: str,
        depth: int,
        extended_partitions: str = "",
        path: str = Paths.DATA_EVENTS_PATH):
    paths = input_paths(date, depth, extended_partitions, path)
    return spark\
        .read\
        .option("basePath", path) \
        .option("badRecordsPath", Paths.SANDBOX_READ_ERRORS_PATH) \
        .parquet(*paths)


def grad2rad(grad: F.col) -> F.col:
    return grad * F.lit(0.0174533)


def distance(lat1_col, lon1_col, lat2_col, lon2_col) -> F.col:
    radius = 6371
    return \
        2 * F.lit(radius) * F.asin(
            F.sqrt(
                F.pow(
                    F.sin((grad2rad(lat1_col) - grad2rad(lat2_col)) / F.lit(2)),
                    F.lit(2)
                ) +
                F.cos(grad2rad(lat1_col)) *
                F.cos(grad2rad(lat2_col)) *
                F.pow(
                    F.sin((grad2rad(lon1_col) - grad2rad(lon2_col)) / F.lit(2)),
                    F.lit(2)
                )
            )
        )