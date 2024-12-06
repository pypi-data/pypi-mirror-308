import sys
import os
import argparse
from schemon.env import loadenv


# Early argument parsing to set the environment before any dependent imports
def parse_args():
    parser = argparse.ArgumentParser(description="data contract command line tool")
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="dev",
        help="Environment to use (e.g., 'local', 'dev', 'prod')",
    )
    # Parse only the -e argument at this point
    args, _ = parser.parse_known_args()
    return args


# The first thing we do is parse the environment argument
args = parse_args()

# Load environment before any other imports that rely on the environment
loadenv(args.env)
env = os.getenv("ENV")
if env:
    print(f"Loaded environment: {os.getenv('ENV')}")

from schemon.migrate import autogenerate_migration, downgrade_database, upgrade_database
from schemon.migration.database import add_database, list_databases, remove_database
from schemon.migration.init import init, remove
from schemon.publish import publish_cli
from schemon.validate import validate_cli, approve_cli


def validate_directory(directory):
    if os.path.isdir(directory):
        return
    else:
        print(f"Error: {directory} is not a valid directory")


def validate_file(file):
    if os.path.isfile(file):
        return
    else:
        print(f"Error: {file} is not a valid file")


def list_all_yaml_files_in_dir(directory):
    """
    Returns a list of all YAML files in the specified directory and its subdirectories.

    Args:
        directory (str): The directory to search for YAML files.

    Returns:
        list: A list of file paths for all YAML files found.
    """
    yaml_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml"):
                yaml_files.append(os.path.join(root, file))
    return yaml_files


def validate_args(args):
    if args.notification == "pr":
        if args.platform == "gitlab":
            if not args.pr_id:
                print(
                    "Error: [--i, --pr_id] is required when [--p, --platform] is 'gitlab'"
                )
                sys.exit(1)
        elif args.platform == "ado":
            if not args.pr_id or not args.repo:
                print(
                    "Error: [--i, --pr_id] and --repo are required when [--p, --platform] is 'ado'"
                )
                sys.exit(1)
        else:
            print("Error: --platform must be either 'gitlab' or 'ado'")
            sys.exit(1)


def main():
    """
    Entry point of the schemon command line tool.

    This function parses the command line arguments, validates the input, and performs the specified command.
    The command can be either "validate" or "publish". The input can be a YAML directory or file.
    """

    parser = argparse.ArgumentParser(description="schemon command line tool")
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="dev",
        help="Environment to use (e.g., 'local', 'dev', 'prod')",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # validate sub-command
    parser_validate = subparsers.add_parser(
        "validate", help="Validate a directory or file"
    )

    validate_group = parser_validate.add_mutually_exclusive_group(required=True)
    validate_group.add_argument(
        "-d", "--directory", type=str, help="The directory to validate"
    )
    validate_group.add_argument("-f", "--file", type=str, help="The file to validate")
    validate_group.add_argument(
        "-a", "--approval", type=str, help="approve or reject a PR validation result"
    )
    parser_validate.add_argument(
        "-n",
        "--notification",
        type=str,
        choices=["console", "pr"],
        help='Notification argument (must be "console" or "pr")',
    )
    parser_validate.add_argument(
        "-p", "--platform", type=str, help="Platform for PR notification"
    )
    parser_validate.add_argument(
        "-i", "--pr_id", type=str, help="PR ID for notification"
    )
    parser_validate.add_argument(
        "-r", "--repo", type=str, help="Repository for PR notification"
    )
    parser_validate.add_argument(
        "-c", "--commit", type=str, help="Commit ID"
    )

    # publish sub-command
    parser_publish = subparsers.add_parser(
        "publish", help="Publish the directory or file after validation"
    )
    publish_group = parser_publish.add_mutually_exclusive_group(required=True)
    publish_group.add_argument(
        "-d", "--directory", type=str, help="The directory to publish"
    )
    publish_group.add_argument("-f", "--file", type=str, help="The file to publish")

    # config sub-command
    parser_config = subparsers.add_parser(
        "config", help="Configure the data contract tool"
    )
    config_subparsers = parser_config.add_subparsers(dest="subcommand")

    # Init subcommand
    init_parser = config_subparsers.add_parser(
        "init", help="Initialize the migration config files"
    )
    init_parser.set_defaults(func=init)

    # Remove subcommand
    init_parser = config_subparsers.add_parser(
        "remove", help="Remove the migration config files"
    )
    init_parser.set_defaults(func=remove)

    # Database subcommand
    db_parser = config_subparsers.add_parser("database")
    db_subparsers = db_parser.add_subparsers(dest="db_command")

    # List databases
    list_parser = db_subparsers.add_parser("list")
    list_parser.set_defaults(func=list_databases)

    # Add database
    add_parser = db_subparsers.add_parser("add")
    add_parser.add_argument("-d", "--db", type=str, help="Name of the database to add")
    add_parser.add_argument("-u", "--url", type=str, help="URL of the database to add")
    add_parser.set_defaults(func=lambda args: add_database(args.db, args.url))

    # Remove database
    remove_parser = db_subparsers.add_parser("remove")
    remove_parser.add_argument(
        "-d", "--db", type=str, help="Name of the database to remove"
    )
    remove_parser.set_defaults(func=lambda args: remove_database(args.db))

    # Migrate sub-command
    migrate_parser = subparsers.add_parser("migrate", help="Migration related commands")
    migrate_subparsers = migrate_parser.add_subparsers(dest="migrate_command")

    # Migrate autogenerate command
    autogenerate_parser = migrate_subparsers.add_parser(
        "autogenerate", help="Autogenerate migration files"
    )
    autogenerate_parser.add_argument("-d", "--db", type=str, help="Database name")
    autogenerate_parser.add_argument(
        "-y", "--yaml_dir", type=str, help="Directory containing YAML files"
    )
    autogenerate_parser.set_defaults(
        func=lambda args: autogenerate_migration(args.db, args.yaml_dir)
    )

    # Migrate upgrade command
    upgrade_parser = migrate_subparsers.add_parser("upgrade", help="Upgrade migration")
    upgrade_parser.add_argument("-d", "--db", type=str, help="Database name")
    upgrade_parser.add_argument(
        "-y", "--yaml_dir", type=str, help="Directory containing YAML files"
    )
    upgrade_parser.add_argument(
        "-r",
        "--revision",
        type=str,
        help="Revision id, default is HEAD",
        required=False,
    )
    upgrade_parser.set_defaults(
        func=lambda args: upgrade_database(args.db, args.yaml_dir, args.revision)
    )

    # Migrate downgrade command
    downgrade_parser = migrate_subparsers.add_parser(
        "downgrade", help="Downgrade migration"
    )
    downgrade_parser.add_argument("-d", "--db", type=str, help="Database name")
    downgrade_parser.add_argument(
        "-y", "--yaml_dir", type=str, help="Directory containing YAML files"
    )
    downgrade_parser.add_argument(
        "-r",
        "--revision",
        type=str,
        help="Revision id, default is HEAD",
        required=False,
    )
    downgrade_parser.set_defaults(
        func=lambda args: downgrade_database(args.db, args.yaml_dir, args.revision)
    )

    if len(sys.argv) < 3:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    files = []

    if args.command == "validate":
        validate_args(args)
        notification = args.notification
        if args.directory:
            validate_directory(args.directory)
            files = list_all_yaml_files_in_dir(args.directory)
        elif args.file:
            validate_file(args.file)
            files = [args.file]
        if notification == "pr":
            ret = validate_cli(
                files,
                notification,
                platform=args.platform,
                pr_id=args.pr_id,
                repo_id=args.repo,
                commit_id=args.commit,
            )
        elif args.approval:
            ret = approve_cli(args.approval, args.pr_id, args.repo, args.commit)
        else:
            ret = validate_cli(files, notification)
    elif args.command == "publish":
        if args.directory:
            validate_directory(args.directory)
            files = list_all_yaml_files_in_dir(args.directory)
        elif args.file:
            validate_file(args.file)
            files = [args.file]
        ret = publish_cli(files)
    elif args.command == "config":
        args.func(args)
        ret = 0
    elif args.command == "migrate":
        args.func(args)
        ret = 0
    else:
        parser.print_help(sys.stderr)
        ret = "Command is not supported"
    sys.exit(ret)


if __name__ == "__main__":
    main()
