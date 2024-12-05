from __future__ import annotations
from functools import wraps
from typing import Type, TypeVar
import time
import os
import json
from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from schemon.common import (
    parse_yaml,
    get_dict_value_by_path,
    logger,
    ValidationReportStatusEnum,
    ApprovalResultEnum,
    TempConstant,
)
from schemon.sqlparser import SqlParser, Table as DepTable, Column as DepColumn
from schemon.model import (
    get_new_id,
    MyBase as Base,
    CLIConfig,
    RegistrySchemaFQN,
    RegistrySchemaTask,
    Revision,
    RevisionLog,
    Session,
    RegistrySchema,
    RegistryField,
    DependTable,
    DependColumn,
    ValidationResult,
    ValidationResultApproval,
)

from schemon.env import loadenv

loadenv()

# subclass of Base
Model = TypeVar("Model", bound=Base)


def transactional(func):
    """
    Decorator that provides transactional behavior to a function.

    This decorator wraps the given function in a transactional context. It creates a new session,
    executes the function within that session, commits the changes if successful, and rolls back
    the changes if an exception occurs. It also provides an option to execute additional functions
    after the commit.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    Raises:
        Exception: If an exception occurs during the execution of the function.

    Example:
        @transactional
        def save_data(data, session):
            # Perform database operations using the provided session
            ...

        # Usage
        save_data(data)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            kwargs["session"] = session
            result = func(*args, **kwargs)
            session.commit()
            if isinstance(result, dict):
                for event in (TransactionEvent.AFTER_COMMIT,):
                    if result.get(event):
                        result.get(event)()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper


def chunk_data(data, chunk_size=int(os.getenv("BULK_INSERT_CHUNK_SIZE"))):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def bulk_insert(session: Session, values: list[Model]) -> None:  # type: ignore
    for chunk in chunk_data(values):
        field_dict_list = [field.to_dict() for field in chunk]
        session.execute(RegistryField.__table__.insert().values(field_dict_list))
        session.flush()


class TransactionEvent:
    """
    Represents a transaction event.

    Attributes:
        AFTER_COMMIT (int): Constant representing the after commit event. Transaction event constants for hooking
    """

    AFTER_COMMIT = 1


def get_latest_registry_schema(session: Session, filters: dict = None) -> RegistrySchema:  # type: ignore
    """
    Retrieve the latest registry schema based on the provided filters.

    Args:
        session (Session): The database session.
        filters (dict, optional): Filters to apply to the query. Defaults to None.

    Returns:
        RegistrySchema: The latest registry schema record that matches the filters.
    """
    query = session.query(RegistrySchema)
    conditions = [RegistrySchema.latest == 1]
    if filters:
        conditions.extend(
            getattr(RegistrySchema, key) == value for key, value in filters.items()
        )
        query = query.filter(and_(*conditions))
    record = query.first()
    return record


def get_model_data(
    my_model: Type[Model],
    session: Session,  # type: ignore
    filters: dict = None,
    single_result: bool = False,
) -> list[Model] | Model:
    """
    Retrieve model data from the database based on the provided filters.

    Args:
        my_model (Model): The model class to query.
        session (Session): The SQLAlchemy session object.
        filters (dict, optional): A dictionary of filters to apply to the query. Each key-value pair represents a filter condition. Defaults to None.
        single_result (bool):  If True, return a single model instance or None if no match is found; otherwise, return a list of matching instances.

    Returns:
        list[Model]: A list of model instances that match the provided filters.
    """
    query = session.query(my_model)
    if filters:
        conditions = [getattr(my_model, key) == value for key, value in filters.items()]
        query = query.filter(and_(*conditions))
    records = query.all()
    if single_result:
        if len(records) > 1:
            logger.warning(
                f"get_model_data: {my_model} query suppose single result but got {len(records)}, return first"
            )
        ret = records[0] if records else None
    else:
        ret = records
    return ret


def update_model_data(my_model: Type[Model], session: Session, update_data: dict, filters: dict) -> int:  # type: ignore
    """Update model data in the database based on the provided filters and data."""
    if not filters:
        logger.warning("update_model_data: filters cannot be empty, do nothing")
        return 0
    query = session.query(my_model)
    conditions = [getattr(my_model, key) == value for key, value in filters.items()]
    query = query.filter(and_(*conditions))
    count = query.update(update_data, synchronize_session="fetch")
    return count


def delete_model_data(my_model: Type[Model], session: Session, filters: dict) -> int:  # type: ignore
    """
    Delete model data from the database based on the provided filters.

    Args:
        my_model (Model): The model class representing the table to delete from.
        session (Session): The SQLAlchemy session object.
        filters (dict, optional): A dictionary of filters to apply to the deletion. Each key-value pair represents a filter condition. Defaults to None.

    Returns:
        int: The number of records deleted.
    """
    query = session.query(my_model)
    if not filters:
        logger.warning("delete_model_data: filters cannot be empty, do nothing")
        return 0
    conditions = [getattr(my_model, key) == value for key, value in filters.items()]
    query = query.filter(and_(*conditions))
    count = query.delete(synchronize_session="fetch")
    return count


def get_registry_fields_by_entity(
    session: Session, entity_name: str, stage: str, env: str  # type: ignore
) -> list[RegistryField]:
    """
    Retrieve the registry fields for a given entity, stage, and environment.

    Args:
        session (Session): The database session.
        entity_name (str): The name of the entity.
        stage (str): The stage of the entity.
        env (str): The environment of the entity.

    Returns:
        list[RegistryField]: A list of registry fields.

    """
    rs = get_latest_registry_schema(
        session, {"entity_name": entity_name, "stage": stage, "env": env}
    )
    rfs = []
    if rs:
        rfs = get_model_data(RegistryField, session, {"schema_id": rs.schema_id})
    return rfs


def get_registry_schema_by_entity(
    session: Session, entity_name: str, stage: str, env: str  # type: ignore
) -> RegistrySchema:
    """
    Retrieves the registry schema for a given entity, stage, and environment.

    Args:
        session (Session): The database session.
        entity_name (str): The name of the entity.
        stage (str): The stage of the schema.
        env (str): The environment of the schema.

    Returns:
        RegistrySchema: The registry schema record that matches the provided filters.

    """
    rs = get_latest_registry_schema(
        session, {"entity_name": entity_name, "stage": stage, "env": env}
    )
    rms = []
    if rs:
        rms = rs
    return rms


@transactional
def add_registry_schema(filepath: str, new_version: str, session: Session):  # type: ignore
    """
    Adds a new registry schema to the database.

    Args:
        filepath (str): The path to the YAML file containing the schema definition.
        new_version (str): The version of the schema to be added.
        session (Session): The database session object.

    Returns:
        dict: A dictionary containing a callback function to be executed after the transaction is committed.
    """
    parsed = parse_yaml(filepath)
    env = os.getenv("ENV")
    stage = parsed["stage"]
    entity_name = parsed["entity"]["name"]

    schema_to_update_previous = (
        session.query(RegistrySchema)
        .filter(
            RegistrySchema.env == env,
            RegistrySchema.stage == stage,
            RegistrySchema.entity_name == entity_name,
            RegistrySchema.latest == 1,
        )
        .all()
    )
    if schema_to_update_previous is not None:
        for schema in schema_to_update_previous:
            schema.previous = 0
    session.flush()

    schema_to_update_latest = (
        session.query(RegistrySchema)
        .filter(
            RegistrySchema.env == env,
            RegistrySchema.stage == stage,
            RegistrySchema.entity_name == entity_name,
            RegistrySchema.latest == 1,
        )
        .all()
    )
    if schema_to_update_latest is not None:
        for schema in schema_to_update_latest:
            schema.latest = 0
            schema.previous = 1
    session.flush()

    content = parsed["_full_content"]
    schema_id = get_new_id()
    registry_schema = RegistrySchema(
        schema_id=schema_id,
        env=os.getenv("ENV"),
        filename=os.path.basename(filepath),
        entity_name=entity_name,
        entity_description=parsed["entity"]["description"],
        stage=parsed["stage"],
        owner_name=parsed["owner"]["name"],
        owner_email=parsed["owner"]["email"],
        platform=parsed["platform"],
        format=parsed["format"],
        type=parsed["type"],
        content=content,
        version=new_version,
        latest=1,
        previous=0,
        created_at=int(time.time()),
    )
    session.add(registry_schema)
    session.flush()

    source_fields: list = parsed["fields"]

    append_config: list = get_dict_value_by_path(
        parsed, "config/transformation_config/append_config"
    )
    if append_config:
        source_fields.extend(append_config)

    dep_tables, dep_columns, select_expressions = get_depend_table_column(parsed)

    registry_field_rows = []
    for i, item in enumerate(source_fields):
        field_name = item["name"]
        # TODO: should an Exception when i >= len()?
        select_expression = (
            select_expressions[i] if i < len(select_expressions) else None
        )
        registry_field_row = RegistryField(
            field_id=get_new_id(),
            schema_id=schema_id,
            name=field_name,
            type=item.get("type"),
            required=item.get("required"),
            nullable=item.get("nullable"),
            unique=item.get("unique"),
            key=item.get("key"),
            primary_key=item.get("primary_key"),
            business_key=item.get("business_key"),
            merge_key = item.get("merge_key"),
            foreign_key=item.get("foreign_key"),
            pd_default=item.get("pd_default"),
            default=item.get("default"),
            description=item.get("description"),
            regex=json.dumps(item.get("regex")),
            example=json.dumps(item.get("example")),
            expression=select_expression,
            dimension=item.get("dimension"),
            incremental=item.get("incremental"),
            created_at=int(time.time()),
        )
        registry_field_rows.append(registry_field_row)
    bulk_insert(session, registry_field_rows)

    if "tasks" in parsed:
        upsert_registry_schema_task(schema_id, parsed["tasks"], session)

    if "DEPENDENCY_ENABLED" in os.environ and os.environ["DEPENDENCY_ENABLED"] == "1":
        depend_tables = [
            DependTable(
                table_id=get_new_id(),
                registry_schema_id=schema_id,
                table_name=d.table_name,
                table_alias=d.alias,
                query_id=d.query_id,
                created_at=int(time.time()),
            )
            for d in dep_tables
        ]
        bulk_insert(session, depend_tables)

        depend_columns = [
            DependColumn(
                column_id=get_new_id(),
                registry_schema_id=schema_id,
                column_name=d.field,
                table_alias=d.table_alias,
                table_names=",".join(d.table_names),
                query_id=d.query_id,
                created_at=int(time.time()),
            )
            for d in dep_columns
        ]
        bulk_insert(session, depend_columns)
    return {
        TransactionEvent.AFTER_COMMIT: lambda: print(
            f"{filepath} schema and field saved successfully with version {new_version}"
        )
    }


def get_depend_table_column(
    parsed: dict,
) -> tuple[list[DepTable], list[DepColumn], list[str]]:
    """
    Get dependent tables & columns from sql in yaml.

    Args:
        parsed (dict): Parsed yaml dict.

    Returns:
        (dep_tables, dep_columns)
    """
    sql_node = get_dict_value_by_path(parsed, "config/transformation_config/sql_config")
    not_found_ret = [], [], []
    if not sql_node:
        return not_found_ret
    for k in ("insert_into", "merge_into"):
        sql = sql_node.get(k)
        if sql:
            break
    if not sql:
        return not_found_ret
    sp = SqlParser(sql)
    return sp.dep_tables, sp.dep_columns, sp.select_expressions


@transactional
def add_cli_config(type: str, key: str, value: str, session: Session):  # type: ignore
    """
    Adds a new CLI config to the database.

    Args:
        type (str): The type of the config.
        key (str): The key of the config.
        value (str): The value of the config.
        session (Session): The database session object.

    Returns:
        dict: A dictionary containing a callback function to be executed after the transaction is committed,
              or a message indicating the config already exists.
    """

    # Check if the combination of type and key already exists in the database
    existing_config = session.query(CLIConfig).filter_by(type=type, key=key).first()

    if existing_config:
        return {
            TransactionEvent.AFTER_COMMIT: lambda: print(
                f"Config with type '{type}' and key '{key}' already exists."
            )
        }

    # Add the new configuration if it doesn't exist
    cli_config_id = get_new_id()
    cli_config = CLIConfig(
        cli_config_id=cli_config_id,
        type=type,
        key=key,
        value=value,
        created_at=int(time.time()),
    )
    session.add(cli_config)
    session.flush()

    return {
        TransactionEvent.AFTER_COMMIT: lambda: print(
            f"{type} and {key} saved successfully"
        )
    }


@transactional
def remove_cli_config(type: str, key: str, session: Session):  # type: ignore
    """
    Removes a CLI config from the database.

    Args:
        type (str): The type of the config.
        key (str): The key of the config.
        session (Session): The database session object.

    Returns:
        dict: A dictionary containing a callback function to be executed after the transaction is committed.
    """
    count = delete_model_data(CLIConfig, session, {"type": type, "key": key})
    message = (
        "{type} and {key} not found"
        if count == 0
        else f"{type} and {key} removed successfully"
    )

    return {TransactionEvent.AFTER_COMMIT: lambda: print(message)}


@transactional
def upsert_registry_schema_fqn(entity_list: list, stage: str, fqn: str, session: Session):  # type: ignore
    """
    Upserts a RegistrySchemaFQN in the database for each entity in the entity_list.

    Args:
        entity_list (list): A list of entity names to associate with the FQN.
        stage (str): The stage of the schema.
        fqn (str): The fully qualified name to upsert.
        session (Session): The database session object.

    Returns:
        dict: A dictionary containing a callback function to be executed after the transaction is committed.
    """
    # Get the environment from the env file or another source
    env = os.getenv("ENV")

    for entity_name in entity_list:
        # Check if a RegistrySchema entry exists for the given entity_name and environment
        registry_schema_entry = (
            session.query(RegistrySchema)
            .filter(RegistrySchema.env == env)
            .filter(RegistrySchema.stage == stage)
            .filter(RegistrySchema.entity_name == entity_name)
            .filter(RegistrySchema.latest == True)
            .first()
        )

        if registry_schema_entry:
            registry_schema_id = registry_schema_entry.schema_id

            # Check if a RegistrySchemaFQN entry exists for the given registry_schema_id
            registry_schema_to_update = (
                session.query(RegistrySchemaFQN)
                .filter(RegistrySchemaFQN.env == env)
                .filter(RegistrySchemaFQN.stage == stage)
                .filter(RegistrySchemaFQN.registry_schema_id == registry_schema_id)
                .first()
            )

            if registry_schema_to_update:
                # Update existing RegistrySchemaFQN
                registry_schema_to_update.fqn = fqn
                registry_schema_to_update.created_at = int(time.time())
                print(
                    f"Updating FQN for entity '{entity_name}' with ID '{registry_schema_id}'"
                )
            else:
                # If no existing RegistrySchemaFQN, create a new one
                registry_schema_fqn = RegistrySchemaFQN(
                    registry_schema_id=registry_schema_id,
                    env=env,
                    stage=stage,
                    fqn=fqn,
                    created_at=int(time.time()),
                )
                session.add(registry_schema_fqn)
                print(
                    f"Creating new FQN for entity '{entity_name}' with ID '{registry_schema_id}'"
                )

        else:
            raise ValueError(
                f"Registry schema not found for entity '{entity_name}', please publish the schema first."
            )

    session.flush()
    return {
        TransactionEvent.AFTER_COMMIT: lambda: print(
            f"FQN upserted successfully for entities: {entity_list}"
        )
    }


def upsert_registry_schema_task(registry_schema_id: str, task_list: list, session: Session):  # type: ignore
    """
    Upserts a RegistrySchemaTask in the database for given entity and task_name_list.

    Args:
        registry_schema_id (str): The schema_id to associate with the entity.
        task_list (list): A list of tasks to associate with the entity.
        session (Session): The database session object.
    """
    # Extract task names from the task_list
    task_names_from_list = {task["name"] for task in task_list}

    # Query all tasks associated with the registry_schema_id
    existing_tasks = (
        session.query(RegistrySchemaTask)
        .filter(RegistrySchemaTask.registry_schema_id == registry_schema_id)
        .all()
    )

    # Extract task names from the existing tasks in the database
    existing_task_names = {task.task_name for task in existing_tasks}

    # Determine tasks to add (present in task_list but not in the database)
    task_names_to_add = task_names_from_list - existing_task_names
    tasks_to_add = [task for task in task_list if task.get("name") in task_names_to_add]

    # Determine tasks to delete (present in the database but not in the task_list)
    tasks_to_delete = existing_task_names - task_names_from_list

    # Add new tasks
    for task in tasks_to_add:
        new_task = RegistrySchemaTask(
            registry_schema_task_id=get_new_id(),
            registry_schema_id=registry_schema_id,
            task_name=task["name"],
            order=task.get("order"),
            full_content=str(task),
            created_at=int(time.time()),
        )
        session.add(new_task)

    # Update existing tasks if order or full_content has changed
    for task in task_list:
        if task["name"] in existing_task_names:
            # Find the existing task in the database
            existing_task = (
                session.query(RegistrySchemaTask)
                .filter(RegistrySchemaTask.registry_schema_id == registry_schema_id)
                .filter(RegistrySchemaTask.task_name == task["name"])
                .first()
            )
            # Check if the order or full_content has changed
            if existing_task and (
                existing_task.order != task.get("order")
                or existing_task.full_content != task
            ):
                # Update the existing task with the new values
                existing_task.order = task.get("order")
                existing_task.full_content = str(task)
                existing_task.created_at = int(time.time())

    # Delete tasks that are no longer in task_list
    for task_name in tasks_to_delete:
        task_to_delete = (
            session.query(RegistrySchemaTask)
            .filter(RegistrySchemaTask.registry_schema_id == registry_schema_id)
            .filter(RegistrySchemaTask.task_name == task_name)
            .first()
        )
        if task_to_delete:
            session.delete(task_to_delete)

    # Flush changes to the database
    session.flush()


def __extract_upgrade_and_downgrade(revision: str):
    import re

    def extract_operations(function: str) -> str:
        """
        Extracts the operations from an Alembic upgrade or downgrade function.

        Args:
            function (str): The full content of the upgrade or downgrade function.

        Returns:
            str: The extracted operations.
        """
        # Define a regex pattern to match the operations
        # This pattern captures lines that start with 'op.' and end with a closing parenthesis
        operations_pattern = r"^\s*op\..+?\)\s*(?=#|$)"
        matches = re.findall(operations_pattern, function, re.MULTILINE | re.DOTALL)
        return "\n".join(match.strip() for match in matches)

    # Extract the full upgrade and downgrade function content
    upgrade_match = re.search(r"def upgrade\(\) -> None:\n(    .+\n)+", revision)
    downgrade_match = re.search(r"def downgrade\(\) -> None:\n(    .+\n)+", revision)

    # Extract only the operations from the full content
    upgrade_content = (
        extract_operations(upgrade_match.group(0)) if upgrade_match else None
    )
    downgrade_content = (
        extract_operations(downgrade_match.group(0)) if downgrade_match else None
    )

    return upgrade_content, downgrade_content


@transactional
def add_revision(revision_id: str, prev_revision_id: str, db: str, revision: str, session: Session):  # type: ignore
    """
    Adds a new revision to the database.

    Args:
        revision_id (str): The ID of the revision.
        db (str): The database key associated with the revision.
        revision (str): The full content of the revision script.
        session (Session): The database session object.

    Returns:
        Revision: The newly created Revision object.
    """
    try:
        # Lookup cli_config_id from CLIConfig table
        cli_config_entry = (
            session.query(CLIConfig).filter_by(key=db, type="database").one()
        )
        cli_config_id = cli_config_entry.cli_config_id
    except NoResultFound:
        raise ValueError(
            f"No CLIConfig entry found for db '{db}' with type 'database'."
        )

    # Extract upgrade and downgrade scripts from revision content
    upgrade, downgrade = __extract_upgrade_and_downgrade(revision)

    # Create a new Revision object
    new_revision = Revision(
        revision_id=revision_id,
        prev_revision_id=prev_revision_id,
        cli_config_id=cli_config_id,
        upgrade=upgrade,
        downgrade=downgrade,
        full_content=revision,
        migrated=False,
        created_at=int(time.time()),
    )

    # Add to session and commit
    session.add(new_revision)

    return {
        TransactionEvent.AFTER_COMMIT: lambda: print(
            f"{revision_id} saved successfully"
        )
    }


@transactional
def update_revision(revision_id: str, updates: dict, session: Session):  # type: ignore
    """
    Updates an existing revision in the database.

    Args:
        revision_id (str): The ID of the revision to update.
        session (Session): The database session object.
        **kwargs: Key-value pairs of fields to update.

    Returns:
        Revision: The updated Revision object.
    """
    try:
        # Retrieve the existing revision
        revision = session.query(Revision).filter_by(revision_id=revision_id).one()

        # Update the fields with new values if provided
        for key, value in updates.items():
            if hasattr(revision, key):
                setattr(revision, key, value)

        return {
            TransactionEvent.AFTER_COMMIT: lambda: print(
                f"{revision_id} updated successfully with {updates}"
            )
        }

    except NoResultFound:
        raise ValueError(f"Revision with ID '{revision_id}' not found.")


def get_revision(session: Session, filters: dict = None) -> Revision:  # type: ignore
    """
    Retrieve a revision based on the provided filters.

    Args:
        session (Session): The database session.
        filters (dict, optional): Filters to apply to the query. Defaults to None.

    Returns:
        Revision: The revision record that matches the filters.
    """
    query = session.query(Revision)
    conditions = []
    if filters:
        conditions.extend(
            getattr(Revision, key) == value for key, value in filters.items()
        )
        query = query.filter(and_(*conditions))
    record = query.first()
    return record


@transactional
def add_revision_log(revision_id: str, command: str, session: Session):  # type: ignore
    """
    Adds a new revision log to the database.

    Args:
        revision_id (str): The ID of the revision.
        command (str): The command that was executed.
        session (Session): The database session object.
    Returns:
        Revision: The newly created Revision Log object.
    """

    revision_log_id = get_new_id()

    # Create a new Revision Log object
    new_revision_log = RevisionLog(
        revision_log_id=revision_log_id,
        revision_id=revision_id,
        command=command,
        timestamp=func.now(),
        created_at=int(time.time()),
    )

    # Add to session and commit
    session.add(new_revision_log)

    return {
        TransactionEvent.AFTER_COMMIT: lambda: print(
            f"Revision log {revision_log_id} saved successfully"
        )
    }


def get_all_revision_ids(session: Session, start_revision_id: str) -> list[str]:  # type: ignore
    """
    Retrieve all revision IDs based on the provided start_revision_id.

    Args:
        session (Session): The SQLAlchemy session object.
        start_revision_id (str): The starting revision ID to find all related revisions.

    Returns:
        list[str]: A list of all related revision IDs.
    """

    def fetch_revisions(revision_id: str, collected_ids: set) -> None:
        # Fetch the current revision details
        current_revision = (
            session.query(Revision).filter_by(revision_id=revision_id).first()
        )

        if current_revision:
            # Add the current revision_id to the set
            collected_ids.add(current_revision.revision_id)

            # Recursively fetch previous revisions if they exist and haven't been visited
            prev_revision_id = current_revision.prev_revision_id
            if prev_revision_id and prev_revision_id not in collected_ids:
                fetch_revisions(prev_revision_id, collected_ids)

    # Use a set to store unique revision IDs
    collected_revision_ids = set()

    # Start the recursive collection from the provided start_revision_id
    fetch_revisions(start_revision_id, collected_revision_ids)

    # Convert the set to a sorted list and return
    return sorted(collected_revision_ids)


def get_latest_registry_schema_task_by_schema(session: Session, schema_id: str) -> [RegistrySchemaTask]:  # type: ignore
    """
    Retrieve the latest registry schema task based on the provided

    Args:
        session (Session): The database session.
        schema_id (str): The schema_id of the schema.

    Returns:
        RegistrySchemaTask list: The latest registry schema task record that matches the filters.
    """
    query = session.query(RegistrySchemaTask).filter(
        RegistrySchemaTask.registry_schema_id == schema_id
    )
    record = query.all()
    return record


@transactional
def save_validation_result(
    pr_id: str,
    repo_id: str,
    commit_id: str,
    result: str,
    status: ValidationReportStatusEnum,
    session: Session,  # type: ignore
):
    pr_id = TempConstant.CLI_PR_ID if not pr_id else pr_id  # TODO: cli pr_id strategy
    update_model_data(
        ValidationResult,
        session,
        {ValidationResult.is_latest: False},
        dict(pr_id=pr_id, repo_id=repo_id),
    )
    validation_result = ValidationResult(
        content=result, pr_id=pr_id, repo_id=repo_id, commit_id=commit_id, status=status, is_latest=True
    )
    session.add(validation_result)


@transactional
def save_validation_result_approval(
    result_id: str,
    approver_id: str,
    approval_result: ApprovalResultEnum,
    session: Session,  # type: ignore
):
    delete_model_data(
        ValidationResultApproval,
        session,
        dict(result_id=result_id, approver_id=approver_id),
    )
    approval_result = ValidationResultApproval(
        result_id=result_id, approver_id=approver_id, approval_result=approval_result
    )
    session.add(approval_result)


def get_validation_result(pr_id: str, repo_id: str, commit_id: str) -> ValidationResult:
    session = Session()
    result = get_model_data(
        ValidationResult,
        session,
        dict(is_latest=True, pr_id=pr_id, repo_id=repo_id, commit_id=commit_id),
        single_result=True,
    )
    return result


def get_validation_results() -> list[ValidationResult]:
    session = Session()
    results = get_model_data(ValidationResult, session, dict(is_latest=True))
    return results


def get_validation_result_approval(
    result_id: str, approver_id: str
) -> ApprovalResultEnum:
    session = Session()
    approval = get_model_data(
        ValidationResultApproval,
        session,
        dict(result_id=result_id, approver_id=approver_id),
        single_result=True,
    )
    return approval.approval_result if approval else None
