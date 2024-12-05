import os
from urllib.parse import parse_qs, urlparse
import yaml
from databricks import sql

from schemon.common import get_dict_value_by_path
from schemon.env import loadenv

loadenv()


def run_sql_query(statements: list):
    """
    Run a list of SQL statements.

    Args:
        statements (list): A list of SQL statements.

    Returns:
        None
    """
    try:
        # Get Databricks SQL connection details from environment variables
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_SQL_WAREHOUSE_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")

        # Establish a connection to the Databricks SQL endpoint
        with sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
        ) as connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Execute each SQL statement
            for statement in statements:
                cursor.execute(statement)
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


def get_table_properties(table_name):
    """
    Get the properties of a Spark table.

    Args:
        table_name (str): The name of the Spark table.

    Returns:
        dict: A dictionary containing the table properties
    """
    try:
        # Get Databricks SQL connection details from environment variables
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_SQL_WAREHOUSE_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")

        # Establish a connection to the Databricks SQL endpoint
        with sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
        ) as connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Define the SQL query to fetch table properties
            query = f"SHOW TBLPROPERTIES {table_name}"

            # Execute the query
            cursor.execute(query)

            # Fetch the results
            properties = {}
            for row in cursor.fetchall():
                properties[row[0]] = row[1]

            # Return the properties dictionary
            return properties
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


def upgrade_table_properties(directory: str, database: str, schema: str):
    """
    Compare the properties of a Spark table with the properties defined in a set of YAML files.

    Args:
        directory (str): The directory containing the YAML files.
        database (str): The database connection string.
        schema (str): The schema name.

    Returns:
        None
    """
    try:
        # Set table property ignore list
        ignore_properties = [
            "delta.columnMapping.maxColumnId",
            "delta.enableDeletionVectors",
            "delta.feature.appendOnly",
            "delta.feature.changeDataFeed",
            "delta.feature.checkConstraints",
            "delta.feature.columnMapping",
            "delta.feature.deletionVectors",
            "delta.feature.generatedColumns",
            "delta.feature.invariants",
            "delta.minReaderVersion",
            "delta.minWriterVersion",
            "clusteringColumns",
            "delta.rowTracking.materializedRowCommitVersionColumnName",
            "delta.rowTracking.materializedRowIdColumnName",
        ]

        # Iterate over each YAML file in the directory
        alter_statement = []
        for filename in os.listdir(directory):
            print(f"\nComparing properties for file: {filename}")
            if filename.endswith(".yaml"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as file:
                    content = yaml.safe_load(file)

                    # Extract properties from YAML
                    yaml_properties = get_dict_value_by_path(
                        content, "config/properties"
                    )

                    # Get Databricks table properties
                    table_full_name = f"{database}.{schema}.{content['entity']['name']}"
                    table_properties = get_table_properties(table_full_name)

                    alter_script_set = []
                    alter_script_unset = []
                    if yaml_properties is not None:
                        # Compare properties
                        for key, value in yaml_properties.items():
                            databricks_value = table_properties.get(key)
                            if databricks_value is None:
                                print(
                                    f"NOTFOUND_IN_TABLE: Key '{key}' not found in table properties."
                                )
                                alter_script_set.append(f"'{key}' = '{value}'")
                            elif value != databricks_value:
                                if (
                                    key == "delta.columnMapping.mode"
                                    and databricks_value == "name"
                                ):
                                    print(
                                        f"CANNOT_CHANGE: Key '{key}' with value {databricks_value} is set in table properties, which cannot be changed."
                                    )
                                    continue
                                print(
                                    f"MISMATCH: Mismatch for key '{key}': YAML value is '{value}', table value is '{databricks_value}'."
                                )
                                alter_script_set.append(f"'{key}' = '{value}'")
                            else:
                                print(f"MATCH: Key '{key}' matches: {value}")

                        # Check for properties to unset
                        for key, value in table_properties.items():
                            if key == "delta.columnMapping.mode" and value == "name":
                                continue
                            if (
                                key not in yaml_properties
                                and key not in ignore_properties
                            ):

                                print(
                                    f"NOTFOUND_IN_YAML: Key '{key}' found in table properties but not in YAML."
                                )
                                alter_script_unset.append(f"'{key}'")

                        # Generate ALTER TABLE SET TBLPROPERTIES script if there are mismatched properties
                        if alter_script_set:
                            alter_statement_set = f"ALTER TABLE {table_full_name} SET TBLPROPERTIES ({', '.join(alter_script_set)});"
                            alter_statement.append(alter_statement_set)

                        # Generate ALTER TABLE UNSET TBLPROPERTIES script if there are properties to remove
                        if alter_script_unset:
                            alter_statement_unset = f"ALTER TABLE {table_full_name} UNSET TBLPROPERTIES ({', '.join(alter_script_unset)});"
                            alter_statement.append(alter_statement_unset)
        if os.getenv("SHOW_SQL") == "1":
            for statement in alter_statement:
                print("SQL: ", statement)
        run_sql_query(alter_statement)
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")
