from schemon.domain.base import Base
from typing import Optional


class Entity(Base):
    def __init__(self, name: str, description: Optional[str] = None):
        if not name:
            raise ValueError("Entity name is required.")
        self.name = name
        self.description = description
