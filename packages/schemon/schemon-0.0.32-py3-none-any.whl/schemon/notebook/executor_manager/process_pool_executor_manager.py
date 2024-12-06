from concurrent.futures import ProcessPoolExecutor
from schemon.notebook.base.executor_manager import ExecutorManager
import multiprocessing

# TODO:
"""
[CONTEXT_ONLY_VALID_ON_DRIVER] 
It appears that you are attempting to reference SparkContext 
from a broadcast variable, action, or transformation. 
SparkContext can only be used on the driver, not in code that it run on workers. 
For more information, see SPARK-5063.
"""


class ProcessPoolExecutorManager(ExecutorManager):
    def __init__(self, max_workers: int = None):
        if max_workers is None:
            # Get the number of CPU cores and use that as the base for max_workers
            cores = multiprocessing.cpu_count()
            max_workers = (
                cores * 2
            )  # Default behavior similar to ThreadPoolExecutorManager
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def execute_tasks(self, tasks):
        futures = [self.executor.submit(task) for task in tasks]
        results = [future.result() for future in futures]
        return results
