from schemon.domain.contract.contract import Contract
from schemon.notebook.base import PlatformManager
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from pyspark.sql import functions as F
from schemon.notebook.engine.spark.spark_type_mapping import SparkTypeMapping
from schemon_python_client.spark.helper.hive import run_hive_query
from schemon.service.contract.config_service import (
    get_insert_into_mode,
    get_sql_config_query,
)
from pyspark.sql.utils import AnalysisException
from pyspark.sql.types import StructType


class HivePlatformManager(PlatformManager):
    def __init__(
        self,
        platform: str,
        format: str,
        database: str,
        table: str = None,
    ):
        super().__init__(platform, format)
        self.database = database
        self.table = table

    def get_connection_details(self) -> dict:
        return {
            "platform": self.get_platform(),
            "format": self.get_format(),
            "database": self.database,
            "table": self.table,
        }

    def truncate(self, spark: SparkSession, contract: Contract):
        database = self.database
        table = self.table if self.table else contract.entity.name
        format = contract.format
        try:
            if format == "parquet" or format == "delta":
                if not spark.catalog.databaseExists(database):
                    return
                if not spark.catalog.tableExists(f"{database}.{table}"):
                    return
                spark.catalog.setCurrentDatabase(database)
                spark.sql(f"TRUNCATE TABLE {database}.{table}")

        except AnalysisException as e:
            if "Table or view not found" in str(e):
                raise ValueError(f"Table {database}.{table} does not exist") from e
            else:
                raise e

    def read(
        self, spark: SparkSession, contract: Contract, kwarg: dict = None
    ) -> SparkDataFrame:
        stage = contract.stage
        entity_name = contract.entity.name
        start_time = self.logger.log_function_start(stage, entity_name)
        database = self.database
        table = self.table if self.table else contract.entity.name
        self.logger.info(
            f"read() - kwarg value: {kwarg}",
            stage,
            entity_name,
        )

        query = get_sql_config_query(contract.config.transformation_config.sql_config)
        query = query.format(database=database, table=table, **kwarg)

        df = run_hive_query(spark, query)

        row_count = df.count()
        self.logger.log_function_end(start_time, stage, entity_name, row_count)
        return df

    def transform(
        self, df: SparkDataFrame, spark: SparkSession, contract: Contract
    ) -> SparkDataFrame:
        df = add_default_values(df, contract)
        return df

    def write(
        self, df: SparkDataFrame, spark: SparkSession, contract: Contract
    ) -> SparkDataFrame:
        type_mapping = SparkTypeMapping()
        database = self.database
        table = self.table if self.table else contract.entity.name
        format = self.format
        mode = get_insert_into_mode(contract.config.transformation_config.sql_config)
        if mode:
            print(
                "write",
                contract.entity.name,
                self.database,
                table,
                format,
                mode,
                df.count(),
            )
            struct_fields = []
            struct_fields.extend(type_mapping.get_struct_fields(contract.fields))
            if contract.config.transformation_config.append_config:
                struct_fields.extend(
                    type_mapping.get_struct_fields(
                        contract.config.transformation_config.append_config
                    )
                )
            struct_type = StructType(
                sorted(struct_fields, key=lambda field: df.columns.index(field.name))
            )
            df = spark.createDataFrame(df.rdd, struct_type)
            spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
            spark.catalog.setCurrentDatabase(database)
            df.write.format(format).mode(mode).saveAsTable(f"{database}.{table}")


# Hive doesn't support default columns, so we need to add them manually
def add_default_values(df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
    type_mapping = SparkTypeMapping()
    defaults = []
    if contract.config.transformation_config.append_config:
        defaults = [
            item
            for item in contract.config.transformation_config.append_config
            if item.default is not None
        ]
    else:
        defaults = [item for item in contract.fields if item.default is not None]
    for item in defaults:
        mapped_type = type_mapping.get_target_type(item.type_)
        if item.default == "system" and item.name == "Version":
            value = contract.version
            df = df.withColumn(item.name, F.lit(value).cast(mapped_type))
        elif item.default == "now":
            value = F.current_timestamp()
            df = df.withColumn(item.name, F.lit(value).cast(mapped_type))
    return df
