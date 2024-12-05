import os
from datetime import datetime
from typing import Dict
from schemon.domain.contract.config import FileNameConfig
from schemon.domain.contract.contract import Contract
from schemon.notebook.base import PlatformManager
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from schemon_python_logger.logger import Logger
from schemon_python_client.spark.credential_manager.unity_catalog_credential_manager import (
    UnityCatalogCredentialManager,
)
from schemon.notebook.engine.spark.spark_type_mapping import SparkTypeMapping
from schemon_python_client.spark.reader.excel import read as read_excel
from schemon_python_client.spark.reader.flatfile import read as read_flatfile
from schemon_python_client.spark.helper.file import (
    remove_leading_slash,
    remove_trailing_slash,
)
from schemon_python_client.spark.helper.unity_catalog import list_files_in_volume
from schemon.service.contract.config_service import (
    get_files_by_file_name_config,
    get_insert_into_mode,
    get_sql_config_query,
)
from pyspark.sql.types import StructType
from schemon_python_client.spark.client.databricks_client import DatabricksClient
from schemon.service.contract.field_service import (
    get_id_column_names,
    get_key_column_name,
    get_merge_column_names,
    get_update_column_names,
    get_value_column_name,
    get_value_column_type,
    get_watermark_column_names,
)


class UnityCatalogPlatformManager(PlatformManager):
    def __init__(
        self,
        spark: SparkSession,
        platform: str,
        format: str,
        database: str,
        schema: str,
        incremental: str = None,
        table: str = None,
        directory_path: str = None,  # directory_path is directory path, used with file_name to get the full qualified path to a file
        directories: list[str] = None,
        extension: str = None,
        file_path: str = None,  # file_path is a full qualified path to a file
        file_name: str = None,  # file_name is used with path to get the full qualified path to a file
        logger: Logger = None,
        parameters: dict = None,
        show_data: dict = None,
        show_sql: bool = False,
        use_sql_for_merge: bool = True,
        use_sql_for_unpivot: bool = False,
        flatfile_reader_options: dict = {},
    ):
        self.database = database
        self.schema = schema
        self.table = table
        self.directory_path = directory_path
        self.directories = directories
        self.extension = extension
        self.file_path = file_path
        self.file_name = file_name
        self.flatfile_reader_options = flatfile_reader_options
        credential_manager = UnityCatalogCredentialManager()
        client = DatabricksClient(
            spark,
            platform,
            format,
            credential_manager,
            show_sql,
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
            "database": self.database,
            "schema": self.schema,
            "table": self.table,
        }

    def truncate(self, contract: Contract):
        stage = contract.stage
        entity_name = contract.entity.name
        database = self.database
        schema = self.schema
        table = self.table if self.table else contract.entity.name

        if self.format == "parquet" or self.format == "delta":
            full_table_name = f"{database}.{schema}.{table}"
            if not self.client.check_table_exists(database, schema, table):
                self.logger.critical(
                    f"Table {full_table_name} does not exist.",
                    stage,
                    entity_name,
                )
            query = f"TRUNCATE TABLE {full_table_name}"
            self.client.execute_query(query)
            self.logger.info(
                f"Table {full_table_name} truncated successfully.",
                stage,
                entity_name,
            )
        else:
            NotImplementedError(
                f"Format {format} is not supported for UnityCatalogPlatformManager"
            )

    def read(self, contract: Contract, kwarg: dict = None) -> SparkDataFrame:
        is_file = self.file_path or self.file_name
        stage = contract.stage
        entity_name = contract.entity.name
        df: SparkDataFrame = None

        if not is_file and (self.format == "parquet" or self.format == "delta"):
            database = self.database
            schema = self.schema
            query = get_sql_config_query(
                contract.config.transformation_config.sql_config
            )
            query = query.format(database=database, schema=schema, **kwarg)
            df = self.client.execute_query(query)

            self.logger.info(
                f"Spark read() - query executed successfully. | {self.format} | Row count: {df.count()}",
                stage,
                entity_name,
            )

        elif is_file:
            append_columns: Dict[str, Dict[str, str]] = {}
            struct_fields = []
            type_mapping = SparkTypeMapping()
            column_names = [field.name for field in contract.fields]
            append_config = contract.config.transformation_config.append_config
            struct_fields.extend(
                type_mapping.get_struct_fields(contract.fields, exclude_default=True)
            )
            if append_config:
                struct_fields.extend(
                    type_mapping.get_struct_fields(append_config, exclude_default=True)
                )
            struct_type = StructType(struct_fields)

            if append_config:
                for append in append_config:
                    append_name = append.name
                    append_type = "int" if append.type_ == "integer" else append.type_
                    pd_default = append.pd_default
                    if pd_default:
                        append_columns[append_name] = {
                            "value": pd_default,
                            "type": (
                                str(append_type)
                                if not isinstance(append_type, str)
                                else append_type
                            ),
                        }
                if append_columns:
                    debug_message = "[Append Config] Adding columns: \n"
                    for column_name, column_config in append_columns.items():
                        debug_message += f"Column: {column_name}, Value: {column_config['value'].strip()}, Type: {column_config['type']}\n"
                    self.logger.debug(
                        debug_message,
                        stage,
                        entity_name,
                    )
            file_name_config: FileNameConfig = getattr(
                contract.config, "file_name_config", None
            )

            matched_files = []
            if self.file_path:
                matched_files.append(self.file_path)
            elif self.file_name:
                self.directory_path = remove_trailing_slash(self.directory_path)
                self.file_name = remove_leading_slash(self.file_name)
                file_path = f"{self.directory_path}/{self.file_name}"
                matched_files.append(file_path)
            else:
                files = list_files_in_volume(
                    self.directory_path, self.directories, self.extension
                )
                if self.extension is None:
                    matched_files = files
                else:
                    matched_files = (
                        get_files_by_file_name_config(files, file_name_config)
                        if file_name_config
                        else files
                    )
            if self.format == "excel":
                excel_parser_config = (
                    contract.config.transformation_config.excel_parser_config
                )
                for file in matched_files:
                    tab_df = read_excel(
                        spark=self.client.spark,
                        file_path=file,
                        sheet_names=excel_parser_config.sheet_name,
                        skip_rows=excel_parser_config.skip_rows,
                        total_rows=excel_parser_config.total_rows,
                        use_columns=excel_parser_config.use_columns,
                        struct_type=struct_type,
                        column_names=column_names,
                        data_types=excel_parser_config.data_types,
                        sheet_names_to_exclude=excel_parser_config.sheet_name_to_exclude,
                        append_columns=append_columns,
                    )

                    if df is None:
                        df = tab_df
                    else:
                        df = df.union(tab_df)

            elif self.format == "csv" or self.format == "tsv" or self.format == "json":
                for file in matched_files:
                    for _, col_spec in append_columns.items():
                        if col_spec["value"] == "metadata.modified":
                            if file_path.startswith("dbfs:/") or file_path.lower().startswith(
                                "/volumnes/"
                            ):
                                col_spec["value"] = datetime.fromtimestamp(os.path.getmtime(file_path))

                    df_single = read_flatfile(
                        spark=self.client.spark,
                        file_path=file,
                        format=self.format,
                        schema=struct_type,
                        append_columns=append_columns,
                        reader_options=self.flatfile_reader_options,
                    )

                    if df is None:
                        df = df_single
                    else:
                        df = df.union(df_single)

            self.logger.info(
                f"Spark read() - file loaded successfully. | {self.format} | Row count: {df.count()}",
                stage,
                entity_name,
            )

        else:
            NotImplementedError(
                f"Format {format} is not supported for UnityCatalogPlatformManager"
            )

        return df

    def transform(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        if self.format == "parquet" or self.format == "delta":
            mode = get_insert_into_mode(
                contract.config.transformation_config.sql_config
            )
            if mode == "unpivot_then_merge":
                df_columns = df.columns
                stage = contract.stage
                entity_name = contract.entity.name
                first_row_contains_header = (
                    contract.config.transformation_config.sql_config.unpivot_then_merge_into.first_row_contains_header
                )
                row_number_column = (
                    contract.config.transformation_config.sql_config.unpivot_then_merge_into.row_number_column
                )
                id_columns = get_id_column_names(
                    contract.fields, df_columns, self.logger, stage, entity_name
                )
                key_column_name = get_key_column_name(
                    contract.fields, df_columns, self.logger, stage, entity_name
                )
                value_column_name = get_value_column_name(
                    contract.fields, df_columns, self.logger, stage, entity_name
                )
                value_column_type = get_value_column_type(
                    contract.fields, df_columns, self.logger, stage, entity_name
                )

                df = self.client.unpivot(
                    df,
                    id_columns,
                    key_column_name,
                    value_column_name,
                    value_column_type,
                    first_row_contains_header,
                    row_number_column,
                    use_sql=self.use_sql_for_unpivot,
                )

                self.logger.info(
                    f"Spark transform() - unpivot executed successfully. Row count: {df.count()}",
                    stage,
                    entity_name,
                )

                self.logger.debug(
                    f"Spark transform() - unpivot operation using {'SQL' if self.use_sql_for_unpivot else 'Python'}",
                    stage,
                    entity_name,
                )

            return df
        else:
            NotImplementedError(
                f"Format {format} is not supported for UnityCatalogPlatformManager"
            )

    def write(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        if self.format == "parquet" or self.format == "delta":
            stage = contract.stage
            entity_name = contract.entity.name

            type_mapping = SparkTypeMapping()
            database = self.database
            schema = self.schema
            table = self.table if self.table else contract.entity.name
            format = self.format
            mode = get_insert_into_mode(
                contract.config.transformation_config.sql_config
            )

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

                struct_fields = []
                struct_fields.extend(
                    type_mapping.get_struct_fields(
                        contract.fields, exclude_default=True
                    )
                )
                if contract.config.transformation_config.append_config:
                    struct_fields.extend(
                        type_mapping.get_struct_fields(
                            contract.config.transformation_config.append_config,
                            exclude_default=True,
                        )
                    )

                struct_type = StructType(
                    sorted(
                        struct_fields, key=lambda field: df.columns.index(field.name)
                    )
                )
                df = self.client.spark.createDataFrame(df.rdd, struct_type)
                self.client.write(df, database, schema, table, mode)

                self.logger.info(
                    f"Spark write() - {mode} executed successfully. Row count: {df.count()}",
                    stage,
                    entity_name,
                )

            elif mode == "merge" or mode == "unpivot_then_merge":
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

                update_set = {
                    f"target.{col}": f"source.{col}" for col in update_columns
                }
                if watermark_columns:
                    for watermark_column in watermark_columns:
                        current_datetime = (
                            f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
                        )
                        update_set[f"target.{watermark_column}"] = current_datetime

                insert_set = {
                    col: f"source.{col}" for col in update_columns + merge_columns
                }

                result = self.client.merge(
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

                self.logger.info(
                    f"Spark write() - merge executed successfully. Row count: {df.count()}",
                    stage,
                    entity_name,
                )

                self.logger.debug(
                    f"Spark write() - merge operation using {'SQL' if self.use_sql_for_merge else 'Delta Python API'}",
                    stage,
                    entity_name,
                )

                # Delta Python API does not return merge metrics yet
                # https://github.com/delta-io/delta/issues/1361
                if result is None:
                    self.logger.warning(
                        "Delta Python API does not return merge metrics yet. https://github.com/delta-io/delta/issues/1361",
                        stage,
                        entity_name,
                    )
                else:
                    merge_metrics = result.first()
                    num_affected_rows = merge_metrics["num_affected_rows"]
                    num_updated_rows = merge_metrics["num_updated_rows"]
                    num_deleted_rows = merge_metrics["num_deleted_rows"]
                    num_inserted_rows = merge_metrics["num_inserted_rows"]
                    self.logger.log_merge_metrics(
                        num_affected_rows,
                        num_updated_rows,
                        num_deleted_rows,
                        num_inserted_rows,
                        stage,
                        entity_name,
                    )
            df.count()  # to avoid lazy execution, so the spark execution is complete.
            return df
        else:
            NotImplementedError(
                f"Format {format} is not supported for UnityCatalogPlatformManager"
            )
