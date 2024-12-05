
from pyspark.sql import SparkSession
from schemon.domain.contract.contract import Contract
from schemon_python_client.spark.base.client import Client

def extract_incremental_kwarg(
    spark: SparkSession,
    platform: str,
    contract: Contract,
    incremental: str,
    database: str,
    schema: str,
    table: str,
    client: Client = None,
):
    incremental_fields = [
        field for field in contract.fields if field.incremental is not None
    ]

    kwarg = {}
    if incremental_fields:
        if len(incremental_fields) > 1:
            raise ValueError("Only one incremental field is allowed")
        else:
            if incremental is not None:
                kwarg["incremental"] = incremental
            else:
                incremental_field = incremental_fields[0]

                # Build and execute the incremental query
                incremental_query = f"SELECT {incremental_field.incremental}({incremental_field.name}) AS Value FROM {database}.{schema}.{table}"
                if platform == "unity catalog":
                    result_row = spark.sql(incremental_query).first()
                elif platform == "azure sql server":
                    result_row = client.execute_query(incremental_query).first()

                if result_row and result_row[0] is not None:
                    incremental_value = result_row[0]
                    kwarg["incremental"] = incremental_value
                else:
                    kwarg["incremental"] = "1900-01-01"  # Default value if no result
    return kwarg