from schemon.domain.base import Base
from schemon_python_logger.logger import Logger
from schemon.notebook.executor_manager import (
    ProcessPoolExecutorManager,
    ThreadPoolExecutorManager,
)
from pyspark.sql import SparkSession
from schemon.notebook.executor_manager.spark_native_executor_manager import (
    SparkNativeExecutorManager,
)
from schemon.notebook.executor_manager.spark_rdd_executor_manager import (
    SparkRDDExecutorManager,
)


class Section(Base):
    def __init__(
        self,
        name,
        spark: SparkSession,
        use_thread_pool: bool,
        use_process_pool: bool,
        use_spark_rdd: bool,
        max_workers: int = None,
        logger: Logger = None,
    ):
        self.name = name
        self.spark = spark
        self.tasks: list = []
        self.logger = logger
        self.max_workers = max_workers

        # Executor managers
        self.executor_manager = None
        self.set_executor_manager(
            use_thread_pool, use_process_pool, use_spark_rdd, spark
        )

    def set_name(self, name):
        self.name = name

    def set_executor_manager(
        self, use_thread_pool, use_process_pool, use_spark_rdd, spark: SparkSession
    ):
        if use_thread_pool:
            self.executor_manager = ThreadPoolExecutorManager(
                spark=self.spark, max_workers=self.max_workers, logger=self.logger
            )
        elif use_process_pool:
            self.executor_manager = ProcessPoolExecutorManager()
        elif use_spark_rdd:
            self.executor_manager = SparkRDDExecutorManager(spark)
        else:
            self.executor_manager = SparkNativeExecutorManager()

    def set_tasks(self, tasks):
        self.tasks = tasks

    def get_executor_manager_type(self):
        return type(self.executor_manager).__name__

    def execute(self):
        return self.executor_manager.execute_tasks(self.tasks)

    def shutdown_executor(self):
        if self.executor_manager:
            self.executor_manager.shutdown_executor()
