import yaml
from pyspark.sql import SparkSession
from delta import *
from schemon.domain.base import Base
from schemon_python_client.spark.helper.common import merge_dict
from schemon_python_logger.print import print_dict


class SparkConfig(Base):
    def __init__(
        self,
        spark: SparkSession,
        app_name: str = None,
        enable_hive_support: bool = False,
        enable_delta_lake: bool = False,
        enable_schemon_spark_listener: bool = False,
        static_configs: dict = {},
        dynamic_configs: dict = {},
    ):
        self.app_name: str = app_name
        self.enable_hive_support: bool = enable_hive_support
        self.enable_delta_lake: bool = enable_delta_lake
        self.enable_schemon_spark_listener: bool = enable_schemon_spark_listener
        self.static_configs: dict = static_configs
        self.dynamic_configs: dict = dynamic_configs
        self.spark: SparkSession = spark

    def load(
        self,
        config_path: str,
        job: str,
        stage: str,
        spark_config_dict: dict = None,
        config_type: str = "yaml",
    ):
        try:
            if config_type == "yaml":
                file_path = f"{config_path}/{job}/{stage}/spark_config.yaml"
                with open(file_path, "r") as file:
                    yaml_data = yaml.safe_load(file)
            elif config_type == "db":                
                config_df = self.spark.sql(f"SELECT value FROM demo.spark_config WHERE job = '{job}' AND stage = '{stage}'").collect()
                config_value = config_df[0]["value"]
                yaml_data = yaml.safe_load(config_value)

            if yaml_data is None:
                raise ValueError("The YAML spark configuration file is empty.")

            if spark_config_dict:
                merge_dict(yaml_data, spark_config_dict)

            # Extract static and dynamic configurations
            spark_config = yaml_data["spark_config"]

            print(f"CONFIG | Spark config:")
            print_dict(spark_config)

            app_name = spark_config["app_name"]
            enable_hive_support = spark_config.get("enable_hive_support", False)
            enable_delta_lake = spark_config.get("enable_delta_lake", False)
            enable_schemon_spark_listener = spark_config.get(
                "enable_schemon_spark_listener", False
            )
            spark_listener_path = spark_config.get("spark_listener_path", False)
            static_configs = spark_config.get("static", {})
            dynamic_configs = spark_config.get("dynamic", {})

            if self.spark is None:
                if enable_delta_lake:
                    spark_builder = SparkSession.builder.appName(
                        app_name
                    ).enableHiveSupport()
                    # Apply static configurations to the Spark session builder
                    for key, value in static_configs.items():
                        spark_builder = spark_builder.config(key, value)
                    if enable_schemon_spark_listener:
                        spark_builder = spark_builder.config(
                            "spark.jars", spark_listener_path
                        )
                        spark_builder = spark_builder.config(
                            "spark.extraListeners",
                            "com.schemon.app.SchemonSparkListener",
                        )

                    spark = configure_spark_with_delta_pip(spark_builder).getOrCreate()
                else:
                    # Create the Spark session with static configurations
                    if enable_hive_support:
                        spark_builder = SparkSession.builder.appName(
                            app_name
                        ).enableHiveSupport()
                    else:
                        spark_builder = SparkSession.builder.appName(app_name)

                    # Apply static configurations to the Spark session builder
                    for key, value in static_configs.items():
                        spark_builder = spark_builder.config(key, value)
                    if enable_schemon_spark_listener:
                        spark_builder = spark_builder.config(
                            "spark.jars", spark_listener_path
                        )
                        spark_builder = spark_builder.config(
                            "spark.extraListeners",
                            "com.schemon.app.SchemonSparkListener",
                        )

                    # Finally, create the Spark session
                    spark = spark_builder.getOrCreate()
            else:
                spark = self.spark

            # Apply dynamic configurations using conf.set()
            for key, value in dynamic_configs.items():
                spark.conf.set(key, value)

            self.app_name = app_name
            self.enable_hive_support = enable_hive_support
            self.enable_delta_lake = enable_delta_lake
            self.enable_schemon_spark_listener = enable_schemon_spark_listener
            self.static_configs = static_configs
            self.dynamic_configs = dynamic_configs
            self.spark = spark

        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return None

        except FileNotFoundError as exc:
            print(f"File not found: {exc}")
            return None
