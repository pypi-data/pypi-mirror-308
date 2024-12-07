import os
import time
from sqlalchemy import (
    create_engine,
    text,
    Column,
    String,
    Integer,
    Boolean,
    TIMESTAMP,
    Text,
    Enum as SqlEnum,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import sessionmaker
from schemon.config import config
from schemon.env import loadenv
from schemon.common import ApprovalResultEnum, ValidationReportStatusEnum

loadenv()

engine = create_engine(
    config.database_uri,
    echo=config.show_sql,
    connect_args=config.connect_args,
)
Session = sessionmaker(bind=engine)


def has_pk_support(*args, **kwargs):
    """use ddl_if make a fake primary key constraint to support hive and pass the sqlalchemy orm check"""
    if os.getenv("DB_TYPE") == "mysql" or os.getenv("DB_TYPE") == "sqlite3":
        return True
    return False


def get_new_id() -> str:
    """
    Generate a new ID based on the current timestamp.

    Returns:
        str: The generated ID.
    """
    time.sleep(1e-6)
    return str(int(time.time() * 1e6))


def get_timestamp() -> int:
    return int(time.time())


@as_declarative()
class MyBase:
    def __repr__(self):
        """generic repr"""
        _d = {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}
        return f"{self.__class__.__name__}({_d})"

    def to_dict(self):
        """get {column: value} dict"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class RegistrySchema(MyBase):
    """
    Represents a registry schema.

    Attributes:
        schema_id (str): The ID of the schema.
        env (str): The environment of the schema.
        filename (str): The filename of the schema.
        stage (str): The stage of the schema.
        entity_name (str): The name of the entity.
        entity_description (str): The description of the entity.
        owner_name (str): The name of the owner.
        owner_email (str): The email of the owner.
        platform (str): The platform of the schema.
        format (str): The format of the schema.
        type (str): The type of the schema.
        content (str): The content of the schema.
        version (str): The version of the schema.
        latest (bool): Indicates if the schema is the latest version.
        previous (bool): Indicates if the schema is the previous version.
        created_at (int): The timestamp when the schema was created.
    """

    __tablename__ = "registry_schema"
    __table_args__ = (PrimaryKeyConstraint("schema_id").ddl_if(None, has_pk_support),)

    schema_id = Column(String(50))
    env = Column(String(10))
    filename = Column(String(500))
    stage = Column(String(50))
    entity_name = Column(String(50))
    entity_description = Column(String(500))
    owner_name = Column(String(100))
    owner_email = Column(String(100))
    platform = Column(String(100))
    format = Column(String(50))
    type = Column(String(50))
    content = Column(Text)
    version = Column(String(10))
    latest = Column(Boolean)
    previous = Column(Boolean)
    created_at = Column(Integer)


class RegistryField(MyBase):
    """
    Represents a field in the registry.

    Attributes:
        field_id (str): The ID of the field.
        schema_id (str): The ID of the schema that the field belongs to.
        name (str): The name of the field.
        type (str): The type of the field.
        required (bool): Indicates if the field is required.
        nullable (bool): Indicates if the field is nullable.
        unique (bool): Indicates if the field is unique.
        key (bool): Indicates if the field is a key.
        primary_key (bool): Indicates if the field is a primary key.
        business_key (bool): Indicates if the field is a business key or part of business keys.
        merge_key(bool): Indicates if the field is a merge key.
        foreign_key (str): The foreign key of the field containing the referencing primary key of another table.
        pd_default (str): The default value of the field in the Pandas DataFrame.
        default (str): The default value of the field.
        description (str): The description of the field.
        regex (str): The regular expression pattern for the field.
        example (str): An example value for the field.
        expression (str): Expression of the field from ETL SQL.
        dimemsion (str): ValidFrom, ValidTo, IsCurrent.
        incremental (str): Incremental field to load incrementally.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "registry_field"
    __table_args__ = (PrimaryKeyConstraint("field_id").ddl_if(None, has_pk_support),)

    field_id = Column(String(50))
    schema_id = Column(String(50))
    name = Column(String(50))
    type = Column(String(50))
    required = Column(Boolean)
    nullable = Column(Boolean)
    unique = Column(Boolean)
    key = Column(Boolean)
    primary_key = Column(Boolean)
    business_key = Column(Boolean)
    merge_key = Column(Boolean)
    foreign_key = Column(String(500))
    pd_default = Column(String(50))
    default = Column(String(50))
    description = Column(String(500))
    regex = Column(String(500))
    example = Column(String(500))
    expression = Column(String(500))
    dimension = Column(String(50))
    incremental = Column(String(50))
    created_at = Column(Integer)


class DependTable(MyBase):
    """
    Represents a table that the registry schema depends on in the ETL process.

    Attributes:
        table_id (str): The ID of the table.
        registry_schema_id (str): The ID of the registry schema that depends on the table.
        table_name (str): Table name in the ETL SQL.
        table_alias (str): Table alias in the ETL SQL.
        query_id (str): The ID of query in the process of SQL parsing, mostly for debug.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "depend_table"
    __table_args__ = (PrimaryKeyConstraint("table_id").ddl_if(None, has_pk_support),)

    table_id = Column(String(50))
    registry_schema_id = Column(String(50))
    table_name = Column(String(50))
    table_alias = Column(String(50))
    query_id = Column(String(50))
    created_at = Column(Integer)


class DependColumn(MyBase):
    """
    Represents a table column that the registry schema depends on in the ETL process.

    Attributes:
        column_id (str): The ID of the column.
        registry_schema_id (str): The ID of the registry schema depending on the field.
        column_name (str): Column name in the ETL SQL.
        table_alias (str): Table alias of the column in the ETL SQL.
        table_names (str): Possible real table names of the column. If the ETL SQL lacks specificity,
                           there would be multiple table names separated by colons.
        query_id (str): The ID of query in the process of SQL parsing, mostly for debug.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "depend_column"
    __table_args__ = (PrimaryKeyConstraint("column_id").ddl_if(None, has_pk_support),)

    column_id = Column(String(50))
    registry_schema_id = Column(String(50))
    column_name = Column(String(50))
    table_alias = Column(String(50))
    table_names = Column(String(200))
    query_id = Column(String(50))
    created_at = Column(Integer)


class RegistrySchemaFQN(MyBase):
    """
    Represents a registry schema fully qualified name.

    Attributes:
        registry_schema_id (str): The ID of the registry schema.
        env (str): The environment of the schema.
        stage (str): The stage of the schema.
        fqn (str): The fully qualified name of the schema used in runtime.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "registry_schema_fqn"
    __table_args__ = (
        PrimaryKeyConstraint("registry_schema_id").ddl_if(None, has_pk_support),
    )

    registry_schema_id = Column(String(50))
    env = Column(String(10))
    stage = Column(String(10))
    fqn = Column(String(500))
    created_at = Column(Integer)


class DMLScript(MyBase):
    """
    Represents a DML script used to populate table in the registry schema.

    Attributes:
        registry_schema_id (str): The ID of the registry schema.
        dml_script (text): The DML script used to populate the table. i.e. INSERT INTO ... MERGE INTO ... VIEW DEFINITION ...
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "dml_script"
    __table_args__ = (
        PrimaryKeyConstraint("registry_schema_id").ddl_if(None, has_pk_support),
    )

    registry_schema_id = Column(String(50))
    dml_script = Column(Text)
    created_at = Column(Integer)


class CLIConfig(MyBase):
    """
    Represents a config.

    Attributes:
        cli_config (str): The ID of the config.
        type (str): The type of the config.
        key (str): The key of the config.
        value (text): The value of the config.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "cli_config"
    __table_args__ = (
        PrimaryKeyConstraint("cli_config_id").ddl_if(None, has_pk_support),
    )
    cli_config_id = Column(String(50))
    type = Column(String(50))
    key = Column(String(50))
    value = Column(Text)
    created_at = Column(Integer)


class Revision(MyBase):
    """
    Represents a revision.

    Attributes:
        revision_id (str): The ID of the revision.
        prev_revision_id (str): The ID of the previous revision.
        cli_config_id (str): The ID of the config.
        upgrade (text): The upgrade script.
        downgrade (text): The downgrade script.
        full_content (text): The full content of the revision.
        migrated (bool): Indicates if the revision has been migrated.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "revision"
    __table_args__ = (PrimaryKeyConstraint("revision_id").ddl_if(None, has_pk_support),)
    revision_id = Column(String(50))
    prev_revision_id = Column(String(50))
    cli_config_id = Column(String(50))
    upgrade = Column(Text)
    downgrade = Column(Text)
    full_content = Column(Text)
    migrated = Column(Boolean)
    created_at = Column(Integer)


class RevisionLog(MyBase):
    """
    Represents a revision log.

    Attributes:
        revision_log_id (str): The ID of the revision log.
        revision_id (str): The ID of the revision.
        command (str): The command of the revision.
        timestamp (TIMESTAMP): The timestamp of the revision.
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "revision_log"
    __table_args__ = (
        PrimaryKeyConstraint("revision_log_id").ddl_if(None, has_pk_support),
    )
    revision_log_id = Column(String(50))
    revision_id = Column(String(50))
    command = Column(String(50))
    timestamp = Column(TIMESTAMP)
    created_at = Column(Integer)


class RegistrySchemaTask(MyBase):
    """
    Represents a registry schema task.

    Attributes:
        registry_schema_task_id (str): The ID of the registry schema task.
        registry_schema_id (str): The ID of the registry schema.
        task_name (str): The name of the task.
        order (int): The order of the task.
        full_content (text): The full content of the task
        created_at (int): The timestamp of when the field was created.
    """

    __tablename__ = "registry_schema_task"
    __table_args__ = (
        PrimaryKeyConstraint("registry_schema_task_id").ddl_if(None, has_pk_support),
    )
    registry_schema_task_id = Column(String(50))
    registry_schema_id = Column(String(50))
    task_name = Column(String(500))
    order = Column(Integer)
    full_content = Column(Text)
    created_at = Column(Integer)


class ValidationResult(MyBase):
    """
    Record validation results
    """
    __tablename__ = "validation_result"
    __table_args__ = (
        PrimaryKeyConstraint("result_id").ddl_if(None, has_pk_support),
    )
    result_id = Column(String(50), default=get_new_id, comment="primary key")
    pr_id = Column(String(50), comment="PR ID, there would be multiple results for one PR")
    repo_id = Column(String(100), comment="repo ID")
    commit_id = Column(String(100), comment="Commit ID, long format. It's different from the short hash.")
    content = Column(Text, comment="validation report in markdown format")
    status = Column(SqlEnum(ValidationReportStatusEnum, native_enum=False), comment="validation report status")
    is_latest = Column(Boolean, default=True, comment="is the latest validation result for the PR")
    created_at = Column(Integer, default=get_timestamp, comment="creation timestamp")


class ValidationResultApproval(MyBase):
    """
    Record validation result approvals
    """
    __tablename__ = "validation_result_approval"
    __table_args__ = (
        PrimaryKeyConstraint("approval_id").ddl_if(None, has_pk_support),
    )
    approval_id = Column(String(50), default=get_new_id, comment="primary key")
    result_id = Column(String(50), nullable=False, comment="validation result ID")
    approver_id = Column(String(50), comment="approval user id")
    approval_result = Column(SqlEnum(ApprovalResultEnum, native_enum=False), comment="approval result")
    comment = Column(Text, comment="approval comment")
    created_at = Column(Integer, default=get_timestamp, comment="creation timestamp")
    updated_at = Column(Integer, onupdate=get_timestamp, comment="update timestamp")


def create_all():
    """
    Creates all the tables defined in the metadata using the provided engine.
    If the database URI starts with "hive", it sets the file format of the "registry_schema" and "registry_field" tables to "orc".
    """
    MyBase.metadata.create_all(engine)
    if config.database_uri.startswith("hive"):
        session = Session()
        for t in ["registry_schema", "registry_field"]:
            session.execute(text(f"alter table {t} set fileformat orc"))
        session.commit()
        session.close()

if __name__ == "__main__":
    create_all()
