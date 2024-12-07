from typing import List, Union
from pyspark.sql.types import (
    StructField,
    StringType,
    IntegerType,
    FloatType,
    BooleanType,
    TimestampType,
    DateType,
)

from schemon.notebook.base import TypeMapping
from schemon.domain.contract.field import Field
from schemon.domain.contract.config import AppendConfig


class SparkTypeMapping(TypeMapping):
    def __init__(self):
        super().__init__()
        self.type_mapping = {
            "int32": IntegerType(),
            "int64": IntegerType(),
            "integer": IntegerType(),
            "object": StringType(),
            "string": StringType(),
            "string[python]": StringType(),
            "float": FloatType(),
            "boolean": BooleanType(),
            "timestamp": TimestampType(),
            "date": DateType(),
            "datetime": TimestampType(),
        }

    def get_struct_fields(
        self, fields: List[Union[Field, AppendConfig]], exclude_default: bool = False
    ) -> List[StructField]:
        """
        Get a list of PySpark StructFields from a list of Fields or AppendConfigs
        """
        struct_fields = []
        for field in fields:
            if field.default and exclude_default:
                continue
            col_name = field.name
            col_type = field.type_
            col_nullable = field.nullable

            # Retrieve the PySpark data type from type_mapping
            spark_type = self.type_mapping.get(col_type)

            if spark_type is None:
                raise ValueError(
                    f"Unsupported data type '{col_type}' for column '{col_name}'"
                )

            # Create a StructField and add it to the fields list
            struct_fields.append(StructField(col_name, spark_type, col_nullable))

        return struct_fields
