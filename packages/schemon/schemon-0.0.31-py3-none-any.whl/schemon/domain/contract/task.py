from schemon.domain.base import Base
from typing import List, Optional


class Task(Base):
    def __init__(self, name: str, order: Optional[int] = None):
        if not name:
            raise ValueError("Task name is required.")
        self.name = name
        self.order = order
