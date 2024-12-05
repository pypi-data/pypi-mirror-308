import yaml
from schemon.notebook.base import Config
from schemon_python_client.spark.helper.common import merge_dict
from schemon_python_logger.print import print_dict
from pyspark.sql import SparkSession


class SparkNotebookConfig(Config):
    def __init__(
        self,
        spark: SparkSession,
        env: str = None,
        type_: str = None,
        name: str = None,
    ):
        self.env: str = env
        self.type_: str = type_
        self.name: str = name
        self.spark: SparkSession = spark

    def load(
        self,
        config_path: str,
        job: str,
        stage: str,
        spark_notebook_config_dict: dict = None,
        config_type: str = "yaml",
    ):
        try:
            if config_type == "yaml":
                file_path = f"{config_path}/{job}/{stage}/spark_notebook_config.yaml"
                with open(file_path, "r") as file:
                    yaml_data = yaml.safe_load(file)
            elif config_type == "db":                
                config_df = self.spark.sql(f"SELECT value FROM demo.spark_notebook_config WHERE job = '{job}' AND stage = '{stage}'").collect()
                config_value = config_df[0]["value"]
                yaml_data = yaml.safe_load(config_value)

            if yaml_data is None:
                raise ValueError("The YAML spark notebook configuration file is empty.")

            if spark_notebook_config_dict:
                merge_dict(yaml_data, spark_notebook_config_dict)

            spark_notebook_config = yaml_data["spark_notebook_config"]

            print(f"CONFIG | Spark notebook config:")
            print_dict(spark_notebook_config)

            log_level = spark_notebook_config.get("log_level", "NOTSET")
            type_ = spark_notebook_config["type_"]
            name = spark_notebook_config["name"]
            env = spark_notebook_config["env"]

            super().__init__(env, type_, name, log_level)

        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return None

        except FileNotFoundError as exc:
            print(f"File not found: {exc}")
            return None