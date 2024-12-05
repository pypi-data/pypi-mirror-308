from schemon.domain.base import Base
from typing import List, Optional


class Rule(Base):
    def __init__(self, rule: str, action: str, description: Optional[str] = None):
        if not rule or not action:
            raise ValueError("Both 'rule' and 'action' must be provided for each rule.")
        self.rule = rule
        self.description = description
        self.action = action


class Expectation(Base):
    def __init__(self, platform: Optional[str], rules: Optional[List[Rule]] = None):
        if not rules:
            raise ValueError(
                "At least one rule must be provided when expectations are not null."
            )
        self.platform = platform
        self.rules = rules
