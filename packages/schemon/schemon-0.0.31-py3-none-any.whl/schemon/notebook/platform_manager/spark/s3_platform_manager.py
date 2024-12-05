from typing import Dict
from datetime import timezone
from schemon.domain.contract.config import FileNameConfig
from schemon.domain.contract.contract import Contract
from schemon.notebook.base.platform_manager import PlatformManager
from schemon_python_logger.logger import Logger
from schemon_python_client.spark.credential_manager.s3_credential_manager import (
    S3CredentialManager,
)
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from schemon.notebook.engine.spark.spark_type_mapping import SparkTypeMapping
from schemon_python_client.spark.reader.excel import read as read_excel
from schemon_python_client.spark.reader.flatfile import read as read_flatfile
from schemon_python_client.spark.client.s3_client import S3Client
from schemon.service.contract.config_service import get_files_by_file_name_config
from schemon_python_client.spark.helper.file import (
    remove_leading_slash,
    remove_trailing_slash,
)
from pyspark.sql.types import StructType


class S3PlatformManager(PlatformManager):
    def __init__(
        self,
        spark: SparkSession,
        platform: str,
        format: str,
        region: str,
        bucket: str,
        prefix: str,
        access_key: str,
        secret_access_key: str,
        delimiter: str = ",",
        file_path: str = None,  # file_path is a full qualified path to a file after bucket. i.e. prefix/file_name
        file_name: str = None,  # file_name is used with path to get the full qualified path to a file
        logger: Logger = None,
        parameters: dict = None,
        show_data: dict = None,
        flatfile_reader_options: dict = {},
    ):
        if format not in ["csv", "tsv", "json", "parquet", "avro", "excel"]:
            raise ValueError(
                "Invalid format. Supported formats are: 'csv', 'tsv', 'json', 'parquet', 'avro', 'excel'."
            )

        self.spark = spark
        self.bucket = bucket
        self.prefix = prefix
        self.file_path = file_path
        self.file_name = file_name
        self.flatfile_reader_options = flatfile_reader_options
        self.delimiter = (
            delimiter if format == "csv" else ("\t" if format == "tsv" else None)
        )

        # Initialize S3CredentialManager and S3Client if platform is S3
        credential_manager = S3CredentialManager(access_key, secret_access_key)
        client = S3Client(spark, credential_manager, platform, format, region)
        self.spark.conf.set("fs.s3a.access.key", access_key)
        self.spark.conf.set("fs.s3a.secret.key", secret_access_key)
        super().__init__(platform, format, logger, parameters, show_data, client)

    def get_connection_details(self) -> dict:
        return {
            "platform": self.get_platform(),
            "format": self.get_format(),
            "bucket": self.bucket,
            "prefix": self.prefix,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "delimiter": self.delimiter,
            "additional_settings": self.kwargs,
        }

    def read(self, contract: Contract, kwarg: dict = None) -> SparkDataFrame:
        stage = contract.stage
        entity_name = contract.entity.name
        df: SparkDataFrame = None

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
            self.prefix = remove_trailing_slash(self.prefix)
            self.file_name = remove_leading_slash(self.file_name)
            file_path = f"{self.prefix}/{self.file_name}"
            matched_files.append(file_path)
        else:
            objects = self.client.list_objects(self.bucket, self.prefix, recursive=True)
            files = [
                obj["Key"] for obj in objects["Contents"] if obj["type_"] == "file"
            ]
            files_with_metadata = [
                {"path": obj["Key"], "metadata.modified": obj["LastModified"]}
                for obj in objects["Contents"]
                if obj.get("type_") == "file"
            ]
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
                        file_path=f"s3a://{self.bucket}/{file}",
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
                            file_with_metadata = [
                                item
                                for item in files_with_metadata
                                if file == item["path"]
                            ]
                            if len(file_with_metadata) == 1:
                                col_spec["value"] = (
                                    file_with_metadata[0]["metadata.modified"]
                                    .astimezone(timezone.utc)
                                    .strftime("%Y-%m-%d %H:%M:%S")
                                )

                    df_single = read_flatfile(
                        spark=self.client.spark,
                        file_path=f"s3a://{self.bucket}/{file}",
                        format=self.format,
                        struct_type=struct_type,
                        append_columns=append_columns,
                        reader_options=self.flatfile_reader_options,
                    )

                    if df is None:
                        df = df_single
                    else:
                        df = df.union(df_single)

        if df is None:
            self.logger.info(
                f"Spark read() - no data found from the source file - matched_files: {matched_files}",
                stage,
                entity_name,
            )
        else:
            self.logger.info(
                f"Spark read() - file loaded successfully. | {self.format} | Row count: {df.count()}",
                stage,
                entity_name,
            )
        return df

    def transform(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        pass

    def write(self, df: SparkDataFrame, contract: Contract) -> SparkDataFrame:
        pass
