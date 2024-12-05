import os
from functools import partial
from typing import List
from schemon.notebook.engine.spark import (
    SparkConfig,
    SparkNotebook,
    SparkSection,
    SparkNotebookConfig,
)
from schemon.notebook.engine.spark.spark_listener import SchemonSparkListner
from schemon.notebook.helper.runner import sort_stages_by_dependency
from schemon.service.notebook.spark.spark_section_config_service import (
    load_spark_section_configs,
)


def run_spark_notebook(config_path: str, target_stage: str = None):
    stages = sort_stages_by_dependency(config_path)
    print(f"Stages to run: {stages}")

    if target_stage is not None and target_stage not in stages:
        raise ValueError(f"Stage {target_stage} not found in the config")

    for stage in stages:
        if target_stage is not None and target_stage != stage:
            continue

    for stage in stages:
        spark_config_file_path = f"{config_path}/{stage}/spark_config.yaml"
        spark_section_config_path = f"{config_path}/{stage}/spark_section_configs.yaml"
        spark_notebook_config_path = f"{config_path}/{stage}/spark_notebook_config.yaml"

        spark_config = SparkConfig()
        spark_config.load(spark_config_file_path)
        spark_session = spark_config.spark
        enable_schemon_spark_listener = spark_config.enable_schemon_spark_listener

        if enable_schemon_spark_listener:
            listener = SchemonSparkListner(spark_session)

        spark_notebook_config = SparkNotebookConfig()
        spark_notebook_config.load(spark_notebook_config_path)

        spark_notebook = SparkNotebook(spark_session, spark_notebook_config)
        logger = spark_notebook.get_logger()
        contracts = spark_notebook.get_contracts()

        spark_sections: List[SparkSection] = []
        spark_section_configs = load_spark_section_configs(
            spark_section_config_path, logger
        )
        for section_config in spark_section_configs:
            spark_section = SparkSection(spark_session, section_config)
            tasks = [partial(spark_section.run, contract) for contract in contracts]
            spark_section.set_tasks(tasks)
            spark_sections.append(spark_section)

        spark_notebook.set_sections(spark_sections)
        results = spark_notebook.run()

        if enable_schemon_spark_listener:
            # listener.write_to_local()
            listener.write_to_s3()

        spark_notebook.shutdown()
        spark_session.stop()


if __name__ == "__main__":
    # project = "kaggle/Football Data from Transfermarkt"
    project = "geomet"
    config_path = f"{os.getcwd()}/src/schemon/runner/spark_runner_config/{project}"
    run_spark_notebook(config_path)
