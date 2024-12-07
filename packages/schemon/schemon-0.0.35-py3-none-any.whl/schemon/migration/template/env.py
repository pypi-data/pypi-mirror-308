import sys
import yaml
import glob
import os
import re
from logging.config import fileConfig
from sqlalchemy import engine_from_config, MetaData, func, text
from sqlalchemy import pool
from sqlalchemy.engine.url import make_url
from alembic.operations.ops import AlterColumnOp, ModifyTableOps, ExecuteSQLOp
from alembic import context
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Date,
    TIMESTAMP,
)
from urllib.parse import urlparse, parse_qs


from schemon.common import get_dict_value_by_path
from schemon.dao import (
    get_registry_schema_by_entity,
    upsert_registry_schema_fqn,
)
from schemon.migration.database import get_database
from schemon.env import loadenv
from schemon.model import Session

loadenv()


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Define a function to fetch the SQLAlchemy URL from a database
# Access custom arguments from the config object
cmd_opts = context.config.get_section("x") or {}
# Extract values
database_url = cmd_opts.get("database_url")
yaml_dir = cmd_opts.get("yaml_dir")
command = cmd_opts.get("command")

database_fqn = ""
config.set_main_option("sqlalchemy.url", database_url)

db_type = os.getenv("DB_TYPE")
if db_type == "databricks":
    parsed_url = urlparse(database_url)
    query_params = parse_qs(parsed_url.query)
    database_fqn = f"{query_params.get('catalog', [None])[0]}.{query_params.get('schema', [None])[0]}"
elif db_type == "mysql":
    match = re.search(r"\/([^\/?]+)(\?|$)", database_url)
    if match:
        database_name = match.group(1)
        database_fqn = database_name
    else:
        raise ValueError(
            f"Could not extract database name from MySQL URL - {database_url}"
        )

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
def load_metadata_from_yaml(directory):
    type_mapping = {
        "string": String,
        "float": Float,
        "integer": Integer,
        "boolean": Boolean,
        "timestamp": TIMESTAMP,
        "date": Date,
        "datetime": DateTime,
    }

    yaml_files = glob.glob(os.path.join(directory, "*.yaml"))

    metadata = MetaData()
    entity_list = []
    stage = ""
    for yaml_file in yaml_files:
        with open(yaml_file, "r") as file:
            schema_definition = yaml.safe_load(file)
            platform = schema_definition.get("platform")
            table_name = schema_definition["entity"]["name"]
            stage = schema_definition["stage"]
            entity_list.append(table_name)
            type_ = schema_definition.get("type")
            fields = schema_definition.get("fields", [])
            append_config = get_dict_value_by_path(
                schema_definition, "config/transformation_config/append_config"
            )
            if append_config:
                fields.extend(append_config)

            # Creating table with metadata
            if type_ == "table":
                columns = []
                for field in fields:
                    field_name = field["name"]
                    field_type = type_mapping.get(field["type"].lower())
                    if db_type in ["mysql"]:
                        if field["type"].lower() == "string":
                            default_length = 255
                            field_type = String(field.get("length", default_length))

                    if field_type is None:
                        raise ValueError(f"Unsupported field type: {field['type']}")

                    column_kwargs = {
                        "nullable": field.get("nullable", True),
                        "primary_key": field.get("primary_key", False),
                        "unique": field.get("unique", False),
                        "server_default": None,
                    }

                    # Handle default values
                    if "default" in field:
                        if field["default"] == "now" and (
                            field["type"] == "timestamp" or field["type"] == "datetime"
                        ):
                            if platform == "sqlserver":
                                column_kwargs["server_default"] = text("getdate()")
                            else:
                                column_kwargs["server_default"] = func.now()
                        elif field["default"] == "system":
                            session = Session()
                            env = os.getenv("ENV")
                            rs = get_registry_schema_by_entity(
                                session, table_name, stage, env
                            )
                            if rs is not None and rs:
                                column_kwargs["server_default"] = rs.version
                        elif field["default"] == "identity":
                            column_kwargs["autoincrement"] = True
                        else:
                            column_kwargs["default"] = field["default"]

                    columns.append(Column(field_name, field_type, **column_kwargs))

                Table(table_name, metadata, *columns)
            elif type_ == "view":
                NotImplemented

    if command == "revision":
        upsert_registry_schema_fqn(entity_list, stage, database_fqn)

    return metadata


if yaml_dir:
    target_metadata = load_metadata_from_yaml(yaml_dir)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        version_table="migration_version",
    )

    with context.begin_transaction():
        context.run_migrations()


def process_revision_directives(context, revision, directives):
    db_url = context.config.get_main_option("sqlalchemy.url")
    dialect_name = make_url(db_url).get_dialect().name
    if dialect_name == "mssql":
        script = directives[0]
        new_operations = []

        # Iterate through upgrade operations and modify 'alter_column' operations
        for op in script.upgrade_ops.ops:
            # Check if the operation is a ModifyTableOps (a batch operation)
            if isinstance(op, ModifyTableOps):
                # Iterate through each operation within the ModifyTableOps
                for table_op in op.ops:
                    if isinstance(table_op, AlterColumnOp):
                        print(f"Processing AlterColumnOp: {table_op}")

                        # Check if the AlterColumnOp has a server_default
                        if table_op.modify_server_default is not None:
                            table_name = table_op.table_name
                            column_name = table_op.column_name

                            # Create the SQL to drop the existing default constraint
                            drop_constraint_sql = f"""
                            DECLARE @constraint_name NVARCHAR(256);
                            SELECT @constraint_name = df.name 
                            FROM sys.default_constraints df
                            JOIN sys.columns col ON df.parent_object_id = col.object_id 
                            AND df.parent_column_id = col.column_id
                            JOIN sys.tables t ON t.object_id = df.parent_object_id
                            WHERE t.name = '{table_name}' AND col.name = '{column_name}';

                            IF @constraint_name IS NOT NULL
                            BEGIN
                                EXEC('ALTER TABLE {table_name} DROP CONSTRAINT ' + @constraint_name);
                            END
                            """

                            # Add the SQL execution operation to a separate list
                            new_operations.append(ExecuteSQLOp(drop_constraint_sql))

            # If it's directly an AlterColumnOp
            elif isinstance(op, AlterColumnOp):
                print(f"Processing AlterColumnOp: {op}")

                # Check if the AlterColumnOp has a server_default
                if op.modify_server_default is not None:
                    table_name = op.table_name
                    column_name = op.column_name

                    # Create the SQL to drop the existing default constraint
                    drop_constraint_sql = f"""
                    DECLARE @constraint_name NVARCHAR(256);
                    SELECT @constraint_name = df.name 
                    FROM sys.default_constraints df
                    JOIN sys.columns col ON df.parent_object_id = col.object_id 
                    AND df.parent_column_id = col.column_id
                    JOIN sys.tables t ON t.object_id = df.parent_object_id
                    WHERE t.name = '{table_name}' AND col.name = '{column_name}';

                    IF @constraint_name IS NOT NULL
                    BEGIN
                        EXEC('ALTER TABLE {table_name} DROP CONSTRAINT ' + @constraint_name);
                    END
                    """

                    # Add the SQL execution operation to a separate list
                    new_operations.append(ExecuteSQLOp(drop_constraint_sql))

        # Insert new operations at the start of the upgrade operations after iteration
        script.upgrade_ops.ops = new_operations + script.upgrade_ops.ops


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            version_table="migration_version",
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
