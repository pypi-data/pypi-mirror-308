from schemon.notebook.base.executor_manager import ExecutorManager


class SparkNativeExecutorManager(ExecutorManager):

    def execute_tasks(self, tasks):
        return [task() for task in tasks]
