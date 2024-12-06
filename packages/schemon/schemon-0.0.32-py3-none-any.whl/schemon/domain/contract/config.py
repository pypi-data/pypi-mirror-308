from typing import List
from schemon.domain.base import Base


class LookupSQL(Base):
    def __init__(self, table, join):
        self.table: str = table
        self.type: str = join.get("type", "inner")
        self.conditions: List = join.get("conditions", [])
        self.lookup_columns: List = join.get("lookup_columns", [])


class UnpivotThenMergeIntoConfig(Base):
    def __init__(self, first_row_contains_header, row_number_column, source_sql):
        self.first_row_contains_header = first_row_contains_header
        self.row_number_column = row_number_column
        self.source_sql = source_sql


class FileNameConfig(Base):
    def __init__(
        self, pattern: str = None, extension: str = None, case_sensitive: bool = False
    ):
        self.pattern = pattern
        self.extension = extension
        self.case_sensitive = case_sensitive


class SQLConfig(Base):
    def __init__(
        self,
        insert_into: str = None,
        merge_into: str = None,
        overwrite: str = None,
        unpivot_then_merge_into: UnpivotThenMergeIntoConfig = None,
        lookup_sql: List[LookupSQL] = [],
    ):
        args = [insert_into, merge_into, overwrite, unpivot_then_merge_into]
        if sum(arg is not None for arg in args) > 1:
            raise ValueError(
                "Only one of `insert_into`, `merge_into`, `unpivot_then_merge_into` or `overwrite` can be present."
            )
        self.insert_into = insert_into
        self.merge_into = merge_into
        self.overwrite = overwrite
        self.unpivot_then_merge_into = unpivot_then_merge_into
        self.lookup_sql = lookup_sql


class ExcelParserConfig(Base):
    def __init__(
        self,
        sheet_name,
        skip_rows,
        total_rows,
        use_columns,
        data_types,
        drop_na_config,
        sheet_name_to_exclude,
    ):
        self.sheet_name = sheet_name
        self.skip_rows = skip_rows
        self.total_rows = total_rows
        self.use_columns = use_columns
        self.data_types = data_types
        self.drop_na_config = drop_na_config
        self.sheet_name_to_exclude = sheet_name_to_exclude


class AppendConfig(Base):
    def __init__(
        self,
        name,
        type_,
        required,
        nullable,
        unique,
        pd_default=None,
        default=None,
        description=None,
        example=None,
    ):
        self.name = name
        self.type_ = type_
        self.required = required
        self.nullable = nullable
        self.unique = unique
        self.pd_default = pd_default
        self.default = default
        self.description = description
        self.example = example


class TransformationConfig(Base):
    def __init__(
        self,
        truncate: bool = False,
        excel_parser_config: ExcelParserConfig = None,
        append_config: List[AppendConfig] = None,
        sql_config: SQLConfig = None,
    ):
        self.truncate = truncate
        self.excel_parser_config = excel_parser_config
        self.append_config = append_config
        self.sql_config = sql_config


class Config(Base):
    def __init__(
        self,
        file_name_config: FileNameConfig = None,
        view_definition=None,
        transformation_config: TransformationConfig = None,
        properties=None,
    ):
        # Ensure view_definition and transformation_config do not co-exist
        if view_definition and transformation_config:
            raise ValueError(
                "`view_definition` and `transformation_config` cannot co-exist."
            )

        self.file_name_config = file_name_config
        self.view_definition = view_definition
        self.transformation_config = transformation_config
        self.properties = properties
