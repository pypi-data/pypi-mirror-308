from schemon.domain.base import Base
from typing import List, Optional


class Field(Base):
    def __init__(
        self,
        name: str,
        type_: str,
        required: bool,
        nullable: bool,
        unique: bool,
        description: str,
        regex: Optional[List[str]] = None,
        example: Optional[List[str]] = None,
        default: Optional[str] = None,
        primary_key: bool = False,
        business_key: bool = False,
        merge_key: bool = False,
        foreign_key: bool = False,
        dimension: str = None,
        incremental: str = None,
    ):
        if not name:
            raise ValueError("Field name is required.")
        if not type_:
            raise ValueError("Field type is required.")

        self.name = name
        self.type_ = type_
        self.required = required
        self.nullable = nullable
        self.unique = unique
        self.description = description
        self.regex = regex
        self.example = example
        self.default = default
        self.primary_key = primary_key
        self.business_key = business_key
        self.merge_key = merge_key
        self.foreign_key = foreign_key
        self.dimension = dimension
        self.incremental = incremental
