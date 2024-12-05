from abc import abstractmethod
from schemon.domain.base import Base


class ExecutorManager(Base):
    @abstractmethod
    def execute_tasks(self, tasks):
        pass

    @abstractmethod
    def shutdown_executor(self):
        pass
