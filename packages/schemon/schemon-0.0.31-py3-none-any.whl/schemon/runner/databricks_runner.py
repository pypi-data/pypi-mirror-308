import os
from pyspark.sql import SparkSession
from functools import partial
from typing import List
from schemon.notebook.engine.spark import (
    SparkConfig,
    SparkNotebook,
    SparkSection,
    SparkNotebookConfig,
)
from schemon.notebook.engine.spark.spark_listener import SchemonSparkListner
from schemon_python_client.spark.helper.databricks import get_all_widgets
from schemon.notebook.helper.runner import (
    get_config_from_widget,
    sort_stages_by_dependency,
)
from schemon.service.notebook.spark.spark_section_config_service import (
    load_spark_section_configs,
)


def run_databricks_notebook(
    spark: SparkSession,
    config_path: str,
    job: str,
    target_stage: str = None,
    config_type: str = "yaml",
):
    widgets: dict = get_all_widgets()
    print(f"CONFIG | Widgets defined: {widgets}")
    spark_config_dict: dict = {}
    spark_notebook_config_dict: dict = {}
    spark_section_configs_dict: dict = {}

    for key, value in widgets.items():
        first_token = key.split(".")[0]
        if first_token == "spark_notebook_config":
            spark_notebook_config_dict[key] = value
        elif first_token.startswith("spark_section_configs"):
            spark_section_configs_dict[key] = value
        elif first_token == "spark_config":
            spark_config_dict[key] = value

    if len(spark_config_dict) > 0:
        spark_config_dict = get_config_from_widget(spark_config_dict)
    if len(spark_notebook_config_dict) > 0:
        spark_notebook_config_dict = get_config_from_widget(spark_notebook_config_dict)
    if len(spark_section_configs_dict) > 0:
        spark_section_configs_dict = get_config_from_widget(spark_section_configs_dict)

    stages = sort_stages_by_dependency(spark, job, config_path, config_type)
    print(f"CONFIG | Stages available: {stages}")
    print(f"CONFIG | Stages to run: {target_stage}")

    if target_stage is not None and target_stage not in stages:
        raise ValueError(f"Stage {target_stage} not found in the config")

    for stage in stages:
        if target_stage is not None and target_stage != stage:
            continue

        spark_config = SparkConfig(spark=spark)
        spark_config.load(config_path, job, stage, spark_config_dict, config_type)
        # enable_schemon_spark_listener = spark_config.enable_schemon_spark_listener

        # TODO: Fix this
        # Databricks throws an error when trying to create a listener
        # if enable_schemon_spark_listener:
        #     listener = SchemonSparkListner(spark_session)

        spark_notebook_config = SparkNotebookConfig(spark=spark)
        spark_notebook_config.load(
            config_path, job, stage, spark_notebook_config_dict, config_type
        )

        spark_notebook = SparkNotebook(spark, spark_notebook_config)
        logger = spark_notebook.get_logger()
        contracts = spark_notebook.get_contracts()
        parameters = spark_notebook.parameters

        spark_sections: List[SparkSection] = []
        spark_section_configs = load_spark_section_configs(
            spark,
            config_path,
            job,
            stage,
            logger,
            spark_section_configs_dict,
            parameters,
            config_type,
        )
        for section_config in spark_section_configs:
            spark_section = SparkSection(spark, section_config, logger)
            tasks = [partial(spark_section.run, contract) for contract in contracts]
            spark_section.set_tasks(tasks)
            spark_sections.append(spark_section)

        spark_notebook.set_sections(spark_sections)
        results = spark_notebook.run()

        # Databricks throws an error when trying to create a listener
        # if enable_schemon_spark_listener:
        #     # listener.write_to_local()
        #     listener.write_to_s3()

        # Databricks spark session is managed by the Databricks runtime, no need to stop it
        # spark_notebook.shutdown()
        # spark_session.stop()