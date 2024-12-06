from datetime import datetime
from schemon.domain.contract.config import LookupSQL
from schemon.domain.contract.contract import Contract
from schemon.notebook.base import PlatformManager
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from pyspark.sql.utils import AnalysisException
from schemon_python_logger.logger import Logger
from schemon_python_client.spark.client.mssql_client import MSSQLClient
from schemon_python_client.spark.credential_manager.mssql_credential_manager import (
    MSSQLCredentialManager,
)
from schemon.notebook.engine.spark.spark_type_mapping import SparkTypeMapping
from schemon_python_client.spark.helper.databricks import get_secret_value
from schemon.service.contract.config_service import (
    get_insert_into_mode,
    get_sql_config_query,
)
from schemon.service.contract.field_service import (
    get_merge_column_names,
    get_update_column_names,
    get_watermark_column_names,
)


class MSSQLPlatformManager(PlatformManager):
    def __init__(
        self,
        spark: SparkSession,
        platform: str,
        format: str,
        database: str,
        schema: str,
        incremental: str = None,
        driver_type: str = "jdbc",  # "jdbc", "spark", "databricks"
        vault: dict = None,
        server: str = None,
        username: str = None,
        password: str = None,
        connection_options: dict = None,
        table: str = None,
        logger: Logger = None,
        parameters: dict = None,
        show_data: dict = None,
        show_sql: bool = False,
        use_sql_for_merge: bool = False,
        use_sql_for_unpivot: bool = False,
    ):
        self.database = database
        self.schema = schema
        self.table = table
        if not server:
            try:
                server_vault = vault["server"]
                server = get_secret_value(
                    scope=server_vault["scope"], key=server_vault["key"]
                )
            except KeyError as e:
                raise ValueError(f"Valut missing key - server. {e}")

        if not username:
            try:
                username_vault = vault["username"]
                username = get_secret_value(
                    scope=username_vault["scope"], key=username_vault["key"]
                )
            except KeyError as e:
                raise ValueError(f"Valut missing key - username. {e}")

        if not password:
            self.password = password
            try:
                password_vault = vault["password"]
                password = get_secret_value(
                    scope=password_vault["scope"], key=password_vault["key"]
                )
            except KeyError as e:
                raise ValueError(f"Valut missing key - password. {e}")

        credential_manager = MSSQLCredentialManager(username, password)
        provider = platform.split(" ")[0]
        client = MSSQLClient(
            spark,
            server,
            database,
            credential_manager,
            driver_type,
            show_sql,
            connection_options,
            provider=provider
        )
        super().__init__(
            platform,
            format,
            logger,
            parameters,
            show_data,
            client,
            incremental,
            use_sql_for_merge,
            use_sql_for_unpivot,
        )

    def get_connection_details(self) -> dict:
        return {
            "platform": self.get_platform(),
            "format": self.get_format(),
            "server": self.server,
            "database": self.database,
            "driver_type": self.client.driver_type,
            "table": self.table,
        }

    def truncate(self, contract: Contract):
        stage = contract.stage
        entity_name = contract.entity.name
        database = self.database
        schema = self.schema
        table = self.table if self.table else contract.entity.name
        try:
            if not self.client.check_database_exists(database):
                self.logger.critical(
                    f"Database {database} does not exist.",
                    stage,
                    entity_name,
                )
                return
            if not self.client.check_table_exists(database, schema, table):
                self.logger.critical(
                    f"Table {database}.{schema}.{table} does not exist.",
                    stage,
                    entity_name,
                )
                return
            self.client.truncate(database, schema, table)
            self.logger.info(
                f"Table {database}.{schema}.{table} truncated successfully.",
                stage,
                entity_name,
            )

        except AnalysisException as e:
            if "Table or view not found" in str(e):
                self.logger.critical(
                    f"Table {database}.{schema}.{table} does not exist.",
                    stage,
                    entity_name,
                )
                raise ValueError(
                    f"Table {database}.{schema}.{table} does not exist"
                ) from e
            else:
                self.logger.critical(
                    f"An error occurred during truncation: {e}",
                    stage,
                    entity_name,
                )
                raise e

    def read(self, contract: Contract, kwarg: dict = None) -> SparkDataFrame:
        database = self.database
        schema = self.schema
        query = get_sql_config_query(contract.config.transformation_config.sql_config)
        query = query.format(database=database, schema=schema, **kwarg)
        df = self.client.execute_query(query)
        return df

    def transform(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        database = self.database
        schema = self.schema
        if contract.config.transformation_config.sql_config:
            lookup_sql_list: list[LookupSQL] | None = (
                contract.config.transformation_config.sql_config.lookup_sql
            )
        else:
            lookup_sql_list = None

        if lookup_sql_list:
            for lookup_sql in lookup_sql_list:
                lookup_table = lookup_sql.table.format(database=database, schema=schema)
                join_type = lookup_sql.type
                join_conditions = lookup_sql.conditions
                lookup_columns = lookup_sql.lookup_columns
                df = self.client.join(
                    df, lookup_table, join_type, join_conditions, lookup_columns
                )

        return df

    def write(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        stage = contract.stage
        entity_name = contract.entity.name
        database = self.database
        schema = self.schema
        table = self.table if self.table else contract.entity.name
        format = self.format
        mode = get_insert_into_mode(contract.config.transformation_config.sql_config)

        if not mode:
            self.logger.error(
                "write() - mode is not defined.",
                stage,
                entity_name,
            )
            raise ValueError("Write mode is not defined")

        if mode == "append" or mode == "overwrite":
            row_count = df.count()
            self.logger.info(
                f"write() - Writing data to {table}. Format: {format}, Row count: {row_count}",
                stage,
                entity_name,
            )

            self.client.write(
                df=df,
                database=database,
                schema=schema,
                table=table,
                mode=mode,
            )

        elif mode == "merge":
            self.logger.info(
                f"write() - Merging data into {table}. Format: {format}",
                stage,
                entity_name,
            )
            merge_columns = get_merge_column_names(
                contract.fields, self.logger, stage, entity_name
            )
            update_columns = get_update_column_names(
                contract.fields, self.logger, stage, entity_name
            )
            watermark_columns = get_watermark_column_names(
                contract.fields, self.logger, stage, entity_name
            )

            merge_condition = " AND ".join(
                [f"target.{col} = source.{col}" for col in merge_columns]
            )
            update_condition = " OR ".join(
                [f"target.{col} != source.{col}" for col in update_columns]
            )

            update_set = {f"target.{col}": f"source.{col}" for col in update_columns}
            if watermark_columns:
                for watermark_column in watermark_columns:
                    current_datetime = (
                        f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
                    )
                    update_set[f"target.{watermark_column}"] = current_datetime

            insert_set = {
                col: f"source.{col}" for col in update_columns + merge_columns
            }

            self.client.merge(
                database,
                schema,
                table,
                merge_condition,
                update_condition,
                update_set,
                insert_set,
                source_df=df,
                use_sql=self.use_sql_for_merge,
            )

        df.count()  # to avoid lazy execution, so the spark execution is complete.
        return df
