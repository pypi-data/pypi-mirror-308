from pyspark.sql import SparkSession
from schemon.notebook.base.executor_manager import ExecutorManager

# TODO:
"""
[CONTEXT_ONLY_VALID_ON_DRIVER] 
It appears that you are attempting to reference SparkContext 
from a broadcast variable, action, or transformation. 
SparkContext can only be used on the driver, not in code that it run on workers. 
For more information, see SPARK-5063.
"""


class SparkRDDExecutorManager(ExecutorManager):
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def execute_tasks(self, tasks):
        # Create an RDD of tasks and run them in parallel
        rdd = self.spark.sparkContext.parallelize(tasks, len(tasks))
        results = rdd.map(
            lambda task: task()
        ).collect()  # Execute tasks in parallel and collect results
        return results
