import yaml
from typing import List
from schemon_python_logger.logger import Logger
from schemon.notebook.platform_manager.spark.hive_platform_manager import (
    HivePlatformManager,
)
from schemon.notebook.platform_manager.spark.s3_platform_manager import (
    S3PlatformManager,
)
from schemon.notebook.platform_manager.spark.mssql_platform_manager import (
    MSSQLPlatformManager,
)
from schemon.notebook.platform_manager.spark.unity_catalog_platform_manager import (
    UnityCatalogPlatformManager,
)
from schemon.notebook.engine.spark import SparkSectionConfig
from schemon_python_client.spark.helper.common import merge_dict
from schemon_python_logger.print import print_dict
from pyspark.sql import SparkSession


def load_spark_section_configs(
    spark: SparkSession,
    config_path: str,
    job: str,
    stage: str,
    logger: Logger,
    spark_section_configs_dict: dict = None,
    parameters: dict = None,
    config_type: str = "yaml",
) -> List[SparkSectionConfig]:
    try:
        spark_section_configs = []
        if config_type == "yaml":
            file_path = f"{config_path}/{job}/{stage}/spark_section_configs.yaml"
            with open(file_path, "r") as file:
                yaml_data = yaml.safe_load(file)
        elif config_type == "db":
            config_df = spark.sql(
                f"SELECT value FROM demo.spark_section_configs WHERE job = '{job}' AND stage = '{stage}'"
            ).collect()
            config_value = config_df[0]["value"]
            yaml_data = yaml.safe_load(config_value)

        if yaml_data is None:
            raise ValueError("The YAML spark notebook configuration file is empty.")

        if spark_section_configs_dict:
            merge_dict(yaml_data, spark_section_configs_dict)

        spark_section_configs_yaml = yaml_data["spark_section_configs"]

        print(
            f"CONFIG | Spark section configs: {len(spark_section_configs_yaml)} section configs"
        )
        for index, spark_section_config_yaml in enumerate(
            spark_section_configs_yaml, start=1
        ):
            print(f"Spark section config: {index}")
            print_dict(spark_section_config_yaml)

        for spark_section_config_yaml in spark_section_configs_yaml:
            name = spark_section_config_yaml["name"]
            use_thread_pool = spark_section_config_yaml.get("use_thread_pool")
            use_process_pool = spark_section_config_yaml.get("use_process_pool")
            use_spark_rdd = spark_section_config_yaml.get("use_spark_rdd")
            max_workers = spark_section_config_yaml.get("max_workers")
            source_platform_manager_config = spark_section_config_yaml[
                "source_platform_manager"
            ]
            target_platform_manager_config = spark_section_config_yaml[
                "target_platform_manager"
            ]

            platform = source_platform_manager_config["platform"].lower()
            format = source_platform_manager_config["format"].lower()
            database = source_platform_manager_config.get("database", None)
            schema = source_platform_manager_config.get("schema", None)
            table = source_platform_manager_config.get("table", None)
            incremental = source_platform_manager_config.get("incremental", None)
            show_data = source_platform_manager_config.get("show_data", None)
            show_sql = source_platform_manager_config.get("show_sql", None)
            directory_path = source_platform_manager_config.get("directory_path", None)
            directories = source_platform_manager_config.get("directories", [])
            extension = source_platform_manager_config.get("extension", None)
            file_path = source_platform_manager_config.get("file_path", None)
            file_name = source_platform_manager_config.get("file_name", None)

            if source_platform_manager_config["platform"] == "hive":
                source_platform_manager = HivePlatformManager(
                    platform=platform,
                    format=format,
                    database=database,
                    table=table,
                )

            elif source_platform_manager_config["platform"] == "unity catalog":
                source_platform_manager = UnityCatalogPlatformManager(
                    spark=spark,
                    platform=platform,
                    format=format,
                    database=database,
                    schema=schema,
                    table=table,
                    incremental=incremental,
                    logger=logger,
                    parameters=parameters,
                    show_data=show_data,
                    directory_path=directory_path,
                    directories=directories,
                    extension=extension,
                    file_path=file_path,
                    file_name=file_name,
                )

            elif source_platform_manager_config["platform"] == "s3":
                source_platform_manager = S3PlatformManager(
                    spark=spark,
                    platform=source_platform_manager_config["platform"],
                    format=source_platform_manager_config["format"],
                    region=source_platform_manager_config["region"],
                    bucket=source_platform_manager_config["bucket"],
                    prefix=source_platform_manager_config["prefix"],
                    delimiter=source_platform_manager_config.get("delimiter", None),
                    access_key=source_platform_manager_config["access_key"],
                    secret_access_key=source_platform_manager_config[
                        "secret_access_key"
                    ],
                    logger=logger,
                    parameters=parameters,
                    show_data=show_data,
                )
            elif (
                source_platform_manager_config["platform"] == "azure sql server"
                or source_platform_manager_config["platform"] == "rds sql server"
            ):
                source_platform_manager = MSSQLPlatformManager(
                    spark=spark,
                    platform=platform,
                    format=format,
                    database=database,
                    schema=schema,
                    driver_type=source_platform_manager_config.get("driver_type", None),
                    vault=source_platform_manager_config.get("vault", None),
                    server=source_platform_manager_config.get("server", None),
                    username=source_platform_manager_config.get("username", None),
                    password=source_platform_manager_config.get("password", None),
                    logger=logger,
                    parameters=parameters,
                    show_data=show_data,
                    show_sql=show_sql,
                    connection_options=source_platform_manager_config.get(
                        "connection_options", None
                    ),
                )
            else:
                raise ValueError("Invalid source platform and/or source format")

            platform = target_platform_manager_config["platform"].lower()
            format = target_platform_manager_config["format"].lower()
            database = target_platform_manager_config.get("database", None)
            schema = target_platform_manager_config.get("schema", None)
            table = target_platform_manager_config.get("table", None)
            show_data = target_platform_manager_config.get("show_data", None)
            show_sql = target_platform_manager_config.get("show_sql", None)
            use_sql_for_merge = target_platform_manager_config.get(
                "use_sql_for_merge", None
            )
            use_sql_for_unpivot = target_platform_manager_config.get(
                "use_sql_for_unpivot", None
            )

            if target_platform_manager_config["format"] == "parquet":
                if target_platform_manager_config["platform"] == "hive":
                    target_platform_manager = HivePlatformManager(
                        platform=platform,
                        format=format,
                        path=target_platform_manager_config["path"],
                        database=database,
                        table=table,
                        pat=target_platform_manager_config.get("pat", None),
                    )
            elif target_platform_manager_config["platform"] == "unity catalog":
                target_platform_manager = UnityCatalogPlatformManager(
                    spark=spark,
                    platform=platform,
                    format=format,
                    database=database,
                    schema=schema,
                    table=table,
                    logger=logger,
                    parameters=parameters,
                    show_data=show_data,
                    use_sql_for_merge=use_sql_for_merge,
                    use_sql_for_unpivot=use_sql_for_unpivot,
                )
            elif (
                target_platform_manager_config["platform"] == "azure sql server"
                or target_platform_manager_config["platform"] == "rds sql server"
            ):
                target_platform_manager = MSSQLPlatformManager(
                    spark=spark,
                    platform=platform,
                    format=format,
                    database=database,
                    schema=schema,
                    table=table,
                    driver_type=target_platform_manager_config.get("driver_type", None),
                    vault=target_platform_manager_config.get("vault", None),
                    server=target_platform_manager_config.get("server", None),
                    username=target_platform_manager_config.get("username", None),
                    password=target_platform_manager_config.get("password", None),
                    logger=logger,
                    parameters=parameters,
                    show_data=show_data,
                    show_sql=show_sql,
                    connection_options=target_platform_manager_config.get(
                        "connection_options", None
                    ),
                )
            else:
                raise ValueError("Invalid target platform")
            spark_section_config = SparkSectionConfig(
                name=name,
                source_platform_manager=source_platform_manager,
                target_platform_manager=target_platform_manager,
                use_thread_pool=use_thread_pool,
                use_process_pool=use_process_pool,
                use_spark_rdd=use_spark_rdd,
                incremental=incremental,
                max_workers=max_workers,
            )
            spark_section_configs.append(spark_section_config)
        return spark_section_configs

    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")
        return None

    except FileNotFoundError as exc:
        print(f"File not found: {exc}")
        return None
