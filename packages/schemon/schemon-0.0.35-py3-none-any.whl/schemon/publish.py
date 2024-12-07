from __future__ import annotations
import os
from schemon.dao import add_registry_schema
from schemon.validate import validate, ValidationResultItemStatusEnum


def publish_cli(filepaths: list[str]):
    """Validate and save YAML schema to the registry database.

    Args:
        filepaths (list[str]): A list of file paths to the YAML schema files.

    Returns:
        None

    This function validates each YAML schema file specified by the filepaths parameter.
    If the validation is successful, the schema is saved to the database.
    If the validation fails or there are warnings, the schema is not saved.
    """

    all_passed = True
    files_to_deploy = []
    print("validate before saving...")
    for filepath in filepaths:
        print(f"- {filepath}")
        validation_result_items, curr_version, new_version = validate(filepath)
        if (
            validation_result_items == ValidationResultItemStatusEnum.FAILED
            or validation_result_items
            == ValidationResultItemStatusEnum.PASSEDWITHWARNING
        ):
            all_passed = False
        if curr_version != new_version:
            files_to_deploy.append({"filepath": filepath, "new_version": new_version})

    override = os.getenv("OVERRIDE_VALIDATION") == "1"
    if all_passed or override:
        if len(files_to_deploy) > 0:
            if override:
                print("Validation failed but override is enabled, save to database\n")
            else:
                print("validate all passed, save to database\n")
            print("files to deploy: ")
            print(
                "\n".join(
                    [
                        f"{file['filepath']} with new version {file['new_version']}"
                        for file in files_to_deploy
                    ]
                )
            )
            print(f"\n" f"results:")
            for file in files_to_deploy:
                add_registry_schema(file["filepath"], file["new_version"])
        else:
            print("no files to deploy")
