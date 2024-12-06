from typing import List
from schemon.domain.contract.field import Field
from schemon_python_logger.logger import Logger


def load_fields(data: List[dict]) -> List[Field]:
    fields = []
    for field_data in data:
        field = Field(
            name=field_data.get("name"),
            type_=field_data.get("type"),
            required=field_data.get("required"),
            nullable=field_data.get("nullable"),
            unique=field_data.get("unique"),
            description=field_data.get("description"),
            regex=field_data.get("regex"),
            example=field_data.get("example"),
            default=field_data.get("default"),
            primary_key=field_data.get("primary_key"),
            business_key=field_data.get("business_key"),
            merge_key=field_data.get("merge_key"),
            foreign_key=field_data.get("foreign_key"),
            dimension=field_data.get("dimension"),
            incremental=field_data.get("incremental"),
        )
        fields.append(field)
    return fields


def get_id_column_names(
    fields: List[Field],
    df_columns: List[str] = [],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> List[str]:
    """
    Get the id column names that are used as the id columns in the unpivot operation
    """
    if df_columns == []:
        if logger is not None:
            logger.error(
                f"get_id_columns() - df_columns is empty",
                stage,
                entity_name,
            )
        raise ValueError("get_id_columns() - df_columns is empty")
    else:
        id_columns = [
            field.name
            for field in fields
            if field.merge_key and field.name in df_columns
        ]
    if logger is not None:
        logger.debug(
            f"get_id_columns() - id_columns: {id_columns}",
            stage,
            entity_name,
        )
    return id_columns


def get_key_column_name(
    fields: List[Field],
    df_columns: List[str] = [],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> str:
    """
    Get the key column name that is used as the key column in the unpivot operation
    """
    if df_columns == []:
        if logger is not None:
            logger.error(
                f"get_key_column_name() - df_columns is empty",
                stage,
                entity_name,
            )
        raise ValueError("get_key_column_name() - df_columns is empty")
    else:
        key_column_name = [
            field.name
            for field in fields
            if field.merge_key and field.name not in df_columns
        ][0]
    if logger is not None:
        logger.debug(
            f"get_key_column_name() - key_column_name: {key_column_name}",
            stage,
            entity_name,
        )
    return key_column_name


def get_value_column_name(
    fields: List[Field],
    df_columns: List[str] = [],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> str:
    """
    Get the value column name that is used as the key column in the unpivot operation
    """
    if df_columns == []:
        if logger is not None:
            logger.error(
                f"get_value_column_name() - df_columns is empty",
                stage,
                entity_name,
            )
        raise ValueError("get_value_column_name() - df_columns is empty")
    else:
        # Should be exactly one column for value
        value_column_name = [
            field.name
            for field in fields
            if field.merge_key != True and field.name not in df_columns
        ][0]
    if logger is not None:
        logger.debug(
            f"get_value_column_name() - value_column_name: {value_column_name}",
            stage,
            entity_name,
        )
    return value_column_name


def get_value_column_type(
    fields: List[Field],
    df_columns: List[str] = [],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> str:
    """
    Get the value column type that is used as the key column in the unpivot operation
    """
    if df_columns == []:
        if logger is not None:
            logger.error(
                f"get_value_column_type() - df_columns is empty",
                stage,
                entity_name,
            )
        raise ValueError("get_value_column_type() - df_columns is empty")
    else:
        # Should be exactly one column for value
        value_column_type = [
            field.type_
            for field in fields
            if field.merge_key != True and field.name not in df_columns
        ][0]
    if logger is not None:
        logger.debug(
            f"get_value_column_type() - value_column_type: {value_column_type}",
            stage,
            entity_name,
        )
    return value_column_type


def get_non_default_fields(
    fields: List[Field],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> list[Field]:
    """
    Get the fields that are not default fields
    """
    non_default_fields = [field for field in fields if not field.default]
    if logger is not None:
        non_default_field_names = [field.name for field in non_default_fields]
        logger.debug(
            f"get_non_default_fields() - non_default_fields: {non_default_field_names}",
            stage,
            entity_name,
        )
    return non_default_fields


def get_merge_column_names(
    fields: List[Field],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> list[str]:
    """
    Get the merge columns that are used as the merge columns in the merge operation
    """
    merge_columns = [field.name for field in fields if field.merge_key]
    if logger is not None:
        logger.debug(
            f"get_merge_column_names() - get_merge_column_names: {merge_columns}",
            stage,
            entity_name,
        )
    return merge_columns


def get_update_column_names(
    fields: List[Field],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> list[str]:
    """
    Get the update columns that are used as the update columns in the merge operation
    """
    update_columns = [
        field.name for field in fields if not field.merge_key and not field.default
    ]
    if logger is not None:
        logger.debug(
            f"get_merge_columns() - get_update_column_names: {update_columns}",
            stage,
            entity_name,
        )
    return update_columns


def get_watermark_column_names(
    fields: List[Field],
    logger: Logger = None,
    stage: str = None,
    entity_name: str = None,
) -> list[str]:
    """
    Get the watermark columns that are used as the watermark columns in the merge operation
    """
    watermark_columns = [field.name for field in fields if field.default == "now"]
    if logger is not None:
        logger.debug(
            f"get_merge_columns() - get_watermark_column_names: {watermark_columns}",
            stage,
            entity_name,
        )
    return watermark_columns
