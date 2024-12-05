from schemon.domain.base import Base
from schemon.domain.contract.contract import Contract
from pyspark.sql import DataFrame as SparkDataFrame


class Store(Base):
    def __init__(self, contract, df):
        self.contract: Contract = contract
        self.df: SparkDataFrame = df
