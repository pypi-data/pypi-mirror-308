import os
import shutil
import schemon.dao
from alembic.config import Config
from alembic import command


def init(args):
    try:
        # Define the base directory for the project
        target_dir = os.getcwd()

        # Define the Migration directory name
        migration_dir = os.path.join(target_dir, "migrations")

        # Define the Migration ini file path
        migration_ini_path = os.path.join(target_dir, "alembic.ini")

        # Create an Alembic config object
        migration_cfg = Config(migration_ini_path)
        migration_cfg.set_main_option("script_location", migration_dir)

        package_directory = get_package_directory()

        custom_template_dir = os.path.join(package_directory, "migration/template")

        # Check if the migrations directory exists, if not, create it
        if not os.path.exists(migration_dir):
            os.makedirs(migration_dir)

        # Initialize the Alembic environment
        command.init(migration_cfg, migration_dir, template=custom_template_dir)

    except Exception as e:
        print(f"An error occurred while initialize migration config files: {e}")
        raise e

    print(f"Migration initialized in {migration_dir}")


def remove(args):
    try:
        current_dir = os.getcwd()
        # Define the Migration directory name
        migration_dir = os.path.join(current_dir, "migrations")

        # Define the Migration ini file path
        migration_ini_path = os.path.join(current_dir, "alembic.ini")

        # Check if the directory exists
        if os.path.exists(migration_dir):
            # Remove the directory and all its contents
            shutil.rmtree(migration_dir)
            print(f"Successfully removed Alembic directory: {migration_dir}")
        else:
            print(f"Directory does not exist: {migration_dir}")

        if os.path.exists(migration_ini_path):
            os.remove(migration_ini_path)
            print(f"Successfully removed Alembic directory: {migration_ini_path}")
        else:
            print(f"File does not exist: {migration_ini_path}")
    except Exception as e:
        print(f"An error occurred while removing Alembic files: {e}")
        raise e

    print(f"Removed migration config files")


def get_package_directory():
    # Define the path to your custom template directory
    import importlib.util

    # Replace 'your_package_name' with the actual package name
    package_name = "schemon"

    # Get the spec for the package
    spec = importlib.util.find_spec(package_name)

    # Get the package's installed directory
    package_directory = spec.origin
    package_directory = package_directory[: package_directory.rfind("/")]

    return package_directory


if __name__ == "__main__":
    init("")
