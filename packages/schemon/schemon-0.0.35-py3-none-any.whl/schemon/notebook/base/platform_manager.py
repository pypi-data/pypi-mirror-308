from abc import abstractmethod
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from schemon.domain.base import Base
from schemon.domain.contract.contract import Contract
from schemon_python_client.spark.base.client import Client
from schemon_python_logger.logger import SchemonPythonLogger


class PlatformManager(Base):
    def __init__(
        self,
        platform: str = None,
        format: str = None,
        logger: SchemonPythonLogger = None,
        show_data: dict = None,
        show_sql: bool = False,
        client: Client = None,
        use_sql_for_merge: bool = True,
        use_sql_for_unpivot: bool = False,
        tokens: dict = {}
    ):
        self.platform = platform
        self.format = format
        self.logger = logger
        self.show_data = show_data
        self.show_sql = show_sql
        self.client = client
        self.use_sql_for_merge = use_sql_for_merge
        self.use_sql_for_unpivot = use_sql_for_unpivot
        self.tokens = tokens

    def get_platform(self) -> str:
        return self.platform

    def get_format(self) -> str:
        return self.format

    @abstractmethod
    def truncate(self, spark: SparkSession, contract: Contract):
        pass

    @abstractmethod
    def read(self, spark: SparkSession, contract: Contract):
        pass

    @abstractmethod
    def transform(self, df: SparkDataFrame, spark: SparkSession, contract: Contract):
        pass

    @abstractmethod
    def write(self, df: SparkDataFrame, spark: SparkSession, contract: Contract):
        pass
