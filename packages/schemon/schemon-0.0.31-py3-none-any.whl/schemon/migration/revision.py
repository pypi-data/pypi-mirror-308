import sys
import os
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine


from schemon.dao import get_all_revision_ids, get_revision
from schemon.migration.database import get_database
from schemon.env import loadenv
from schemon.model import Session

loadenv()


def get_last_applied_revision_id(database_url: str):
    """
    Retrieves the last applied Alembic revision ID from the specified database.

    Args:
        database_url (str): The database URL.

    Returns:
        str: The last applied revision ID from the database, or None if no revisions are applied.

    Raises:
        ValueError: If the database cannot be found or connected.
    """
    try:
        # Create an engine and connect to the database
        engine = create_engine(database_url)
        with engine.connect() as connection:
            # Create a MigrationContext object
            context = MigrationContext.configure(
                connection, opts={"version_table": "migration_version"}
            )

            # Get the current revision from the database
            current_revision = context.get_current_revision()

        return current_revision

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running get_last_applied_revision_id: {e}")
        sys.exit(1)


def get_revision_full_content(revision_id: str):
    """
    Retrieves the full content of a revision script from the database.

    Args:
        revision_id (str): The revision ID to retrieve.

    Returns:
        str: The full content of the revision script.
    """
    try:
        session = Session()
        revision = get_revision(session, {"revision_id": revision_id})
        if revision is None:
            return None
        return revision.full_content
    except Exception as e:
        print(f"An error occurred during get_revision_full_content: {e}")
        sys.exit(1)


def get_revisions(revision_id: str):
    """
    Retrieves the full content of a revision script from the database.

    Args:
        revision_id (str): The revision ID to retrieve.

    Returns:
        str: The full content of the revision script.
    """
    try:
        session = Session()
        revision_ids = get_all_revision_ids(session, revision_id)
        return revision_ids
    except Exception as e:
        print(f"An error occurred during get_revisions: {e}")
        sys.exit(1)
