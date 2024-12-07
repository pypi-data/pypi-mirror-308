from pyspark.sql import SparkSession
from schemon.domain.contract.contract import Contract
from schemon_python_client.spark.base.client import Client
from schemon_python_logger.print import print_sql


def extract_incremental_value(
    spark: SparkSession,
    platform: str,
    contract: Contract,
    database: str,
    schema: str,
    table: str,
    client: Client = None,
    show_sql: bool = False,
):
    incremental_fields = [
        field for field in contract.fields if field.incremental is not None
    ]

    if incremental_fields:
        if len(incremental_fields) > 1:
            raise ValueError("Only one incremental field is allowed")
        else:
            incremental_field = incremental_fields[0]

            # Build and execute the incremental query
            incremental_query = f"SELECT {incremental_field.incremental}({incremental_field.name}) AS Value FROM {database}.{schema}.{table}"
            if show_sql:
                print_sql(incremental_query)
            if platform == "unity catalog":
                result_row = spark.sql(incremental_query).first()
            elif platform == "azure sql server":
                result_row = client.execute_query(incremental_query).first()

            if result_row and result_row[0] is not None:
                incremental_value = result_row[0]
                return incremental_value
            else:
                return "1900-01-01"  # Default value if no result
    else:
        return None
