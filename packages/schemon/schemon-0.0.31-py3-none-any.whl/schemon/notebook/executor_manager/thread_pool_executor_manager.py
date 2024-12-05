from concurrent.futures import ThreadPoolExecutor
from schemon.notebook.base.executor_manager import ExecutorManager
from schemon_python_logger.logger import Logger


class ThreadPoolExecutorManager(ExecutorManager):
    def __init__(
        self,
        spark,
        max_workers: int = None,
        logger: Logger = None,
    ):
        cores = spark.sparkContext.defaultParallelism
        if max_workers is None:
            max_workers = cores * 5  # this is the default behavior
            log_message = f"ThreadPoolExecutorManager | cores: {cores} | max_workers: {max_workers} | default x5"
        else:
            log_message = f"ThreadPoolExecutorManager | cores: {cores} | max_workers: {max_workers} | overridden"

        if logger:
            logger.info(log_message)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute_tasks(self, tasks):
        futures = [self.executor.submit(task) for task in tasks]
        results = [future.result() for future in futures]
        return results
