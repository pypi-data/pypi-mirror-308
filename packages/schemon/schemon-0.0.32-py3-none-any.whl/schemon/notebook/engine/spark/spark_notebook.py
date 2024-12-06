from typing import List
from pyspark.sql import SparkSession
from schemon.notebook.base.notebook import Notebook
from schemon.notebook.engine.spark.spark_section import SparkSection
from schemon.notebook.engine.spark.spark_notebook_config import SparkNotebookConfig


class SparkNotebook(Notebook):
    def __init__(
        self,
        spark: SparkSession,
        config: SparkNotebookConfig,
    ):
        self.spark: SparkSession = spark
        self.config: SparkNotebookConfig = config
        name = config.get_name()
        type_ = config.get_type()
        super().__init__(type_, config, name)

    def set_spark_session(self, spark):
        self.spark = spark

    def get_contracts(self):
        return super().get_contracts()

    def add_section(self, section):
        sections = self.get_sections()
        sections.append(section)
        self.set_sections(sections)

    def set_sections(self, sections):
        super().set_sections(sections)

    def get_sections(self) -> List[SparkSection]:
        return super().get_sections()

    def run(self):
        results = []
        for section in self.get_sections():
            results.extend(section.execute())
        return results
    
    def shutdown(self):
        results = []
        for section in self.get_sections():
            results.append(section.shutdown_executor())
        return results