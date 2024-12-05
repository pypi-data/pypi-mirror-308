import fnmatch
from typing import List
from schemon.domain.contract.config import (
    FileNameConfig,
    SQLConfig,
    TransformationConfig,
    Config,
    ExcelParserConfig,
    AppendConfig,
    UnpivotThenMergeIntoConfig,
    LookupSQL,
)


def load_config(data: dict) -> Config:
    file_name_config_data = data.get("file_name_config")
    view_definition = data.get("view_definition")
    transformation_config_data = data.get("transformation_config")
    properties = data.get("properties")

    transformation_config = None
    if transformation_config_data:
        transformation_config = load_transformation_config(transformation_config_data)

    file_name_config = None
    if file_name_config_data:
        file_name_config = load_file_name_config(file_name_config_data)

    return Config(
        file_name_config=file_name_config,
        view_definition=view_definition,
        transformation_config=transformation_config,
        properties=properties,
    )


def load_transformation_config(data: dict) -> TransformationConfig:
    truncate = data.get("truncate")
    excel_parser_config_data = data.get("excel_parser_config")
    append_config_data = data.get("append_config")
    sql_config_data = data.get("sql_config")

    excel_parser_config = None
    if excel_parser_config_data:
        excel_parser_config = load_excel_parser_config(excel_parser_config_data)

    append_config = None
    if append_config_data:
        append_config = load_append_config(append_config_data)

    sql_config = None
    if sql_config_data:
        sql_config = load_sql_config(sql_config_data)

    return TransformationConfig(
        truncate=truncate,
        excel_parser_config=excel_parser_config,
        append_config=append_config,
        sql_config=sql_config,
    )


def load_file_name_config(data: dict) -> FileNameConfig:
    if not data:
        return FileNameConfig()

    pattern = data.get("pattern")
    extension = data.get("extension")
    case_sensitive = data.get("case_sensitive")

    return FileNameConfig(
        pattern=pattern,
        extension=extension,
        case_sensitive=case_sensitive,
    )


def load_lookup_sql(data: List[dict]) -> List[LookupSQL]:
    lookup_sql_list = []

    for item in data:
        table = item.get("table")
        join = item.get("join")

        lookup_sql = LookupSQL(
            table=table,
            join=join,
        )
        lookup_sql_list.append(lookup_sql)

    return lookup_sql_list


def load_unpivot_then_merge_into_config(data: dict) -> UnpivotThenMergeIntoConfig:
    first_row_contains_header = data.get("first_row_contains_header")
    row_number_column = data.get("row_number_column")
    source_sql = data.get("source_sql")

    return UnpivotThenMergeIntoConfig(
        first_row_contains_header=first_row_contains_header,
        row_number_column=row_number_column,
        source_sql=source_sql,
    )


def load_sql_config(data: dict) -> SQLConfig:
    insert_into = data.get("insert_into")
    merge_into = data.get("merge_into")
    overwrite = data.get("overwrite")
    unpivot_then_merge_into: UnpivotThenMergeIntoConfig = None
    lookup_sql: LookupSQL = None

    unpivot_then_merge_into_config = data.get("unpivot_then_merge_into")
    if unpivot_then_merge_into_config:
        unpivot_then_merge_into = load_unpivot_then_merge_into_config(
            unpivot_then_merge_into_config
        )

    lookupSQL_config = data.get("lookup_sql")
    if lookupSQL_config:
        lookup_sql = load_lookup_sql(lookupSQL_config)

    return SQLConfig(
        insert_into=insert_into,
        merge_into=merge_into,
        overwrite=overwrite,
        unpivot_then_merge_into=unpivot_then_merge_into,
        lookup_sql=lookup_sql,
    )


def load_excel_parser_config(data: dict) -> ExcelParserConfig:
    sheet_name = data.get("sheet_name")
    skip_rows = data.get("skip_rows")
    total_rows = data.get("total_rows")
    use_columns = data.get("use_columns")
    data_types = data.get("data_types")
    drop_na_config = data.get("drop_na_config")
    sheet_name_to_exclude = data.get("sheet_name_to_exclude")

    return ExcelParserConfig(
        sheet_name=sheet_name,
        skip_rows=skip_rows,
        total_rows=total_rows,
        use_columns=use_columns,
        data_types=data_types,
        drop_na_config=drop_na_config,
        sheet_name_to_exclude=sheet_name_to_exclude,
    )


def load_append_config(data: List[dict]) -> List[AppendConfig]:
    append_configs = []

    for item in data:
        name = item.get("name")
        type_ = item.get("type")
        required = item.get("required")
        nullable = item.get("nullable")
        unique = item.get("unique")
        pd_default = item.get("pd_default")
        default = item.get("default")
        description = item.get("description")
        example = item.get("example")

        append_config = AppendConfig(
            name=name,
            type_=type_,
            required=required,
            nullable=nullable,
            unique=unique,
            pd_default=pd_default,
            default=default,
            description=description,
            example=example,
        )

        append_configs.append(append_config)

    return append_configs


def get_sql_config_query(sql_config: SQLConfig) -> str:
    query = None

    if sql_config.insert_into is not None:
        query = sql_config.insert_into
    elif sql_config.merge_into is not None:
        query = sql_config.merge_into
    elif sql_config.overwrite is not None:
        query = sql_config.overwrite
    elif sql_config.unpivot_then_merge_into is not None:
        query = sql_config.unpivot_then_merge_into.source_sql
    else:
        raise ValueError(
            "All of 'insert_into', 'merge_into', 'unpivot_then_merge_into' and 'overwrite' are None. A valid query must be provided."
        )

    return query


def get_files_by_file_name_config(
    files: list, file_name_config: FileNameConfig
) -> list:
    matched_files = []
    for file in files:
        file_name_with_extension: str = file.split("/")[-1]
        file_name: str = file_name_with_extension.split(".")[0]
        extension: str = file_name_with_extension.split(".")[-1]
        if file_name_config.extension and extension != file_name_config.extension:
            continue
        if file_name_config.pattern:
            if file_name_config.case_sensitive:
                if fnmatch.fnmatch(file_name, file_name_config.pattern):
                    matched_files.append(file)
            else:
                if fnmatch.fnmatchcase(
                    file_name.lower(), file_name_config.pattern.lower()
                ):
                    matched_files.append(file)
    return matched_files


def get_insert_into_mode(sql_config: SQLConfig):
    if sql_config is None:
        return "append"
    if sql_config.insert_into:
        return "append"
    elif sql_config.overwrite:
        return "overwrite"
    elif sql_config.merge_into:
        return "merge"
    elif sql_config.unpivot_then_merge_into:
        return "unpivot_then_merge"
    else:
        return None
