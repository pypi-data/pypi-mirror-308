from typing import List, Optional

from schemon.domain.base import Base
from schemon.domain.contract.task import Task
from schemon.domain.contract.field import Field
from schemon.domain.contract.expectation import Expectation
from schemon.domain.contract.config import Config
from schemon.domain.contract.entity import Entity
from schemon.domain.contract.owner import Owner


class Contract(Base):
    def __init__(
        self,
        stage: str,
        owner: Owner,
        entity: Entity,
        platform: str,
        format: str,
        type_: str,
        tasks: List[Task],
        fields: List[Field],
        expectations: Optional[Expectation],
        config: Config,
        version: str,
    ):
        if not stage:
            raise ValueError("Stage is required.")

        if platform not in [
            "mysql",
            "sqlserver",
            "hive",
            "unity catalog",
            "azure sql server",
            "rds sql server",
            "s3",
        ]:
            raise ValueError(
                f"Platform must be one of: mysql, sqlserver, hive, unity catalog, azure sql server, rds sql server, s3. Got: {platform}"
            )

        if format not in ["delta", "parquet", "orc", "avro", "json", "csv", "native"]:
            raise ValueError(
                f"Format must be one of: delta, parquet, orc, avro, json, csv, native. Got: {format}"
            )

        if type_ not in ["table", "view"]:
            raise ValueError("Type must be either 'table' or 'view'.")

        self.stage = stage
        self.owner = owner
        self.entity = entity
        self.platform = platform
        self.format = format
        self.type = type_
        self.tasks = tasks
        self.fields = fields
        self.expectations = expectations
        self.config = config
        self.version = version
