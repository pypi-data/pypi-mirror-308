from pyspark.sql import DataFrame

from mx_stream_core.infrastructure.spark import spark

from .base import BaseDataSource

class SparkDeltaDataSource(BaseDataSource):
    def __init__(self, delta_path: str, schema) -> None:
        self.schema = schema
        self.delta_path = delta_path

    def get(self) -> DataFrame:
        try:
            return spark.read.format('delta').load(self.delta_path)
        except Exception as e:
            return spark.createDataFrame(data=[], schema=self.schema)
