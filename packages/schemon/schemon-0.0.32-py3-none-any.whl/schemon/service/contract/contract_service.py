import yaml
from typing import List
from sqlalchemy import and_

from schemon.domain.contract import Contract
from schemon.common import get_dict_value_by_path
from schemon.model import RegistrySchema, Session, RegistrySchemaTask
from schemon.service.contract.config_service import load_config
from schemon.service.contract.expectation_service import load_expectations
from schemon.service.contract.task_service import load_tasks
from schemon.service.contract.field_service import load_fields
from schemon.service.contract.owner_service import load_owner
from schemon.service.contract.entity_service import load_entity


def _parse_contract(yaml_data, version):
    """
    A common function to initialize the Contract class using the parsed YAML content.
    """
    owner = load_owner(get_dict_value_by_path(yaml_data, "owner"))

    entity = load_entity(get_dict_value_by_path(yaml_data, "entity"))

    tasks = load_tasks(get_dict_value_by_path(yaml_data, "tasks"))

    fields = load_fields(get_dict_value_by_path(yaml_data, "fields"))

    expectations = load_expectations(get_dict_value_by_path(yaml_data, "expectations"))

    config = load_config(get_dict_value_by_path(yaml_data, "config"))

    contract = Contract(
        stage=get_dict_value_by_path(yaml_data, "stage"),
        owner=owner,
        entity=entity,
        platform=get_dict_value_by_path(yaml_data, "platform"),
        format=get_dict_value_by_path(yaml_data, "format"),
        type_=get_dict_value_by_path(yaml_data, "type"),
        tasks=tasks,
        fields=fields,
        expectations=expectations,
        config=config,
        version=version,
    )

    return contract


def load_contract_from_yaml(file_path):
    """
    Function to load YAML content from a file and initialize the Contract.
    """
    with open(file_path, "r") as file:
        yaml_data = yaml.safe_load(file)

    return _parse_contract(yaml_data)


def load_contract_from_db(filters: dict = None) -> Contract:
    """
    Function to load YAML content from the database and initialize the Contract.

    Args:
        filters (dict, optional): Filters to apply to the query. Defaults to None.

    Returns:
        Contract: The initialized Contract object based on the content column.
    """
    session = Session()
    query = session.query(RegistrySchema)  # Assuming RegistrySchema is your table class
    conditions = [
        RegistrySchema.latest == 1
    ]  # Modify as per your logic for filtering the latest record

    # Add filters to the query if provided
    if filters:
        conditions.extend(
            getattr(RegistrySchema, key) == value for key, value in filters.items()
        )
    query = query.filter(and_(*conditions))

    # Retrieve the first matching record
    record = query.first()

    # If a record is found, parse the content column
    if record and hasattr(record, "content"):
        yaml_content = record.content
        version = record.version
        yaml_data = yaml.safe_load(yaml_content)
        return _parse_contract(yaml_data, version)
    else:
        raise ValueError("No matching record found or 'content' column is missing.")


def load_contract_from_db_by_task_name(
    task_name: str, env: str = "dev"
) -> List[Contract]:
    """
    Function to load records from the database based on a task name by joining
    RegistrySchemaTask with RegistrySchema and return a list of RegistrySchema objects.

    Args:
        task_name (str): The task name to filter RegistrySchemaTask.

    Returns:
        List[RegistrySchema]: A list of RegistrySchema objects.
    """
    session = Session()

    # Join RegistrySchema with RegistrySchemaTask on schema_id and filter by task_name
    query = (
        session.query(RegistrySchema)
        .join(
            RegistrySchemaTask,
            RegistrySchema.schema_id == RegistrySchemaTask.registry_schema_id,
        )
        .filter(
            RegistrySchemaTask.task_name == task_name,
            RegistrySchema.latest == 1,
            RegistrySchema.env == env,
        )
        .order_by(RegistrySchemaTask.order.asc())
    )

    # Retrieve all matching records
    records = query.all()
    if not records or len(records) == 0:
        raise ValueError("No matching records found.")

    # Return the list of Contract objects
    contracts = []
    for record in records:
        if hasattr(record, "content"):
            yaml_content = record.content
            version = record.version
            yaml_data = yaml.safe_load(yaml_content)
            contracts.append(_parse_contract(yaml_data, version))
        else:
            raise ValueError("No matching record found or 'content' column is missing.")
    return contracts
