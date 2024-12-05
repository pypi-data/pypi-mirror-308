import sys
import configparser
from schemon.dao import add_cli_config, remove_cli_config, get_model_data
from schemon.model import CLIConfig, Session


def get_database(filters: dict) -> CLIConfig:
    session = Session()
    try:
        databases = get_model_data(CLIConfig, session, filters)
        if not databases:
            print(
                f"Database configuration for '{list(filters.values())}' does not exist."
            )
        else:
            return databases[0]
    finally:
        session.close()


def list_databases(args):
    session = Session()
    try:
        databases = get_model_data(CLIConfig, session, {})
        if not databases:
            print("No database configuration found in the database.")
        else:
            print("Database configurations in database:")
            for database in databases:
                print(f" - {database.key}: {database.value}")
    finally:
        session.close()


def add_database(db_name, db_url):
    add_cli_config("database", db_name, db_url)


def remove_database(db_name):
    remove_cli_config(type="database", key=db_name)


if __name__ == "__main__":
    list_databases()
