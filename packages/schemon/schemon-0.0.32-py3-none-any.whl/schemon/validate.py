from __future__ import annotations
import os
import yaml
from schemon.common import (
    parse_yaml,
    ValidationTypeEnum,
    ValidationResultItemStatusEnum,
    ApprovalResultEnum,
    TempConstant,
    ReturnWithMessage,
)
from schemon.model import Session
from typing import Tuple
from schemon.dao import (
    get_latest_registry_schema,
    get_latest_registry_schema_task_by_schema,
    get_registry_schema_by_entity,
    get_registry_fields_by_entity,
    save_validation_result,
)
from schemon.validator import (
    ValidationResult,
    compare_fields,
    compare_schema,
    compare_config,
    compare_expectation,
    ValidationResultItem,
    compare_tasks,
    handle_validation_results,
)
from prettytable import PrettyTable
from schemon.notification.ado import create_pr_thread_ado, requeue_pr_pipeline_ado
from schemon.notification.gitlab import create_pr_thread_gitlab
from schemon.notification.composer import generate_validation_report, get_report_status

from schemon import dao


def validate_cli(
    filepaths: list[str],
    notification: str,
    platform: str = None,
    repo_id: str = None,
    commit_id: str = None,
    pr_id: str = None,
):
    """
    Validates the given filepaths and prints the validation results.

    Args:
        filepaths (list[str]): A list of filepaths to be validated.
        notification (str): The notification destination to be sent to.
        platform (str, optional): The git repository platform.
        repo_id (str, optional): The repository ID.
        commit_id (str, optional): The commit ID.
        pr_id (str, optional): The pull request ID.

    Returns:
        ValidationResultEnum: The validation result.

    """
    notification_items = []
    validation_passed = True

    pr_id = TempConstant.CLI_PR_ID if pr_id is None else pr_id
    repo_id = TempConstant.REPO_ID if repo_id is None else repo_id
    commit_id = TempConstant.COMMIT_ID if commit_id is None else commit_id
    if validation_result_approved(pr_id, repo_id, commit_id):
        print(f"Validation result for PR #{pr_id} already approved for the latest commit")
        return 0

    for filepath in filepaths:
        table = PrettyTable()
        table.align = "l"
        table.field_names = [
            "Passed",
            "Warning",
            "Name",
            "Type",
            "Validation Type",
            "Message",
        ]
        validation_result_items, curr_version, new_version = validate(filepath)

        if any(
            item.status == ValidationResultItemStatusEnum.FAILED
            for item in validation_result_items
        ):
            validation_passed = False

        print("\n")
        handle_validation_results(
            filepath,
            curr_version,
            new_version,
            validation_result_items,
            notification_items,
            table,
        )
        print(table)

    if notification == "pr":
        if platform == "ado":
            newline = "\n"

            print("Sending validation result to Azure DevOps...")
            report = generate_validation_report(notification_items, newline)
            response = create_pr_thread_ado(repo_id, pr_id, report)
            print("Azure Devops response: ", response)
        elif platform == "gitlab":
            project_id = os.getenv("GITLAB_PROJECT_ID")
            pat = os.getenv("GITLAB_PAT")
            newline = "   \n"

            print("Sending notification to Gitlab...")
            report = generate_validation_report(notification_items, newline)
            response = create_pr_thread_gitlab(project_id, pr_id, pat, report)
            print("Gitlab response", response)
    # save report in database for approval
    result_status = get_report_status(notification_items)
    report_md = generate_validation_report(notification_items, "\n\n")
    save_validation_result(pr_id, repo_id, commit_id, report_md, result_status)

    if not validation_passed and os.getenv("OVERRIDE_VALIDATION") == "1":
        print("Validation failed but override is enabled")
        return 0
    elif not validation_passed:
        print("Validation failed")
        return 1
    print("Validation passed")
    return 0


def validation_result_approved(pr_id: str, repo_id: str, commit_id: str) -> bool:
    """Returns True if the validation result has been approved, False otherwise."""
    result = dao.get_validation_result(pr_id, repo_id, commit_id)
    if not result:
        return False
    result_approval = dao.get_validation_result_approval(
        result.result_id, TempConstant.APPROVER_ID
    )
    if not result_approval:
        return False
    return ApprovalResultEnum.approved == result_approval


def validate(filepath: str) -> Tuple[list[ValidationResultItem], str, str]:
    """Validate YAML with registry database.

    Args:
        filepath (str): The path to the YAML file to be validated.

    Returns:
        Tuple[list[ValidationResultItem], str, str]: A tuple containing the validation results,
        the current version, and the new version.

    """

    validation_result_items = []
    parsed = parse_yaml(filepath)
    entity_name = parsed["entity"]["name"]
    stage = parsed["stage"]
    env = os.getenv("ENV")
    session = Session()
    rs = get_registry_schema_by_entity(session, entity_name, stage, env)

    if rs:
        validation_result_items = compare(session, parsed)
    else:
        validation_result_items.append(
            ValidationResultItem(
                entity_name,
                "entity",
                True,
                False,
                ValidationResultItemStatusEnum.PASSEDWITHNEW,
                ValidationTypeEnum.NEW,
                f"no previous registry schema data for entity [{entity_name}]",
            )
        )
    curr_version, new_version = get_new_version(
        session, validation_result_items, entity_name, stage, env
    )
    return validation_result_items, curr_version, new_version


def compare(
    session: Session,  # type: ignore
    source: dict[str:dict],
) -> list[ValidationResultItem]:
    """
    Compares the source schema, fields, config, and expectations with the target schema, fields, config, and expectations.

    Args:
        session (Session): The database session.
        source (dict[str:dict]): The source schema, fields, config, and expectations.

    Returns:
        list[ValidationResultItem]: A list of validation results.
    """

    entity_name = source["entity"]["name"]
    stage = source["stage"]
    env = os.getenv("ENV")

    # compare schema
    rs = get_registry_schema_by_entity(session, entity_name, stage, env)
    full_content = yaml.safe_load(rs.content)
    source_schema_dict = {
        "stage": source["stage"],
        "entity_name": source["entity"]["name"],
        "entity_description": source["entity"]["description"],
        "owner_name": source["owner"]["name"],
        "owner_email": source["owner"]["email"],
        "platform": source["platform"],
        "format": source["format"],
        "type": source["type"],
    }
    target_schema_dict = {
        "stage": rs.stage,
        "entity_name": rs.entity_name,
        "entity_description": rs.entity_description,
        "owner_name": rs.owner_name,
        "owner_email": rs.owner_email,
        "platform": rs.platform,
        "format": rs.format,
        "type": rs.type,
    }
    validation_result_items = compare_schema(source_schema_dict, target_schema_dict)

    # compare tasks
    source_tasks_dict_list = source.get("tasks", [])
    target = get_latest_registry_schema_task_by_schema(session, rs.schema_id)
    target_task_dict_list = [
        {
            "name": task.task_name,
            **({"order": task.order} if task.order is not None else {}),
        }
        for task in target
    ]
    validation_result_items.extend(
        compare_tasks(source_tasks_dict_list, target_task_dict_list)
    )

    # compare fields
    source_field_dict = source
    target = get_registry_fields_by_entity(session, entity_name, stage, env)
    target_field_dict = {d.name: vars(d) for d in target}
    validation_result_items.extend(compare_fields(source_field_dict, target_field_dict))

    # compare config
    source_config_dict = source.get("config")
    target_config_dict = full_content.get("config")
    validation_result_items.extend(
        compare_config(source_config_dict, target_config_dict)
    )

    # compare expectation
    source_expectation_dict = source.get("expectations")
    target_expectation_dict = full_content.get("expectations")
    validation_result_items.extend(
        compare_expectation(source_expectation_dict, target_expectation_dict)
    )

    return validation_result_items


def get_new_version(
    session: Session,  # type: ignore
    validation_result_items: list[ValidationResult],
    entity_name: str,
    stage: str,
    env: str,
) -> Tuple[str, str]:
    """
    Determines the new version based on the validation results.

    Args:
        session (Session): The session object used for retrieving the latest schema.
        validation_result_items (list[ValidationResult]): A list of validation results.
        entity_name (str): The entity name.
        stage (str): The stage.
        env (str): The environment.

    Returns:
        Tuple[str, str]: A tuple containing the current version and the new version.

    Raises:
        None

    """
    default_version = "1.0"
    is_major = None

    latest_schema = get_latest_registry_schema(
        session, {"entity_name": entity_name, "stage": stage, "env": env}
    )
    if latest_schema is not None:
        curr_version = latest_schema.version

    if not validation_result_items:
        return curr_version, curr_version
    elif (
        len(validation_result_items) == 1
        and validation_result_items[0].validation_type == ValidationTypeEnum.NEW
    ):
        return "New entity", default_version
    elif any(not result.passed for result in validation_result_items):
        is_major = True
    elif any(result.passed and result.warning for result in validation_result_items):
        is_major = False
    else:
        return "INVALID_VERSION"

    return curr_version, increment_version(is_major, curr_version)


def increment_version(is_major: bool, curr_version: str) -> str:
    """
    Increments the version number based on the given parameters.

    Args:
        is_major (bool): A boolean value indicating whether to increment the major version.
        curr_version (str): The current version number in the format "major.minor".

    Returns:
        str: The new version number after incrementing.

    """
    major, minor = map(int, curr_version.split("."))

    if is_major:
        major += 1
        minor = 0
    else:
        minor += 1

    new_version = f"{major}.{minor}"
    return new_version


def approve(
    pr_id: str, repo_id: str, approval_result: ApprovalResultEnum, commit_id: str
) -> ReturnWithMessage:
    # TODO: handle gitlab, ado, github
    result = dao.get_validation_result(pr_id, repo_id, commit_id)
    if not pr_id:
        return ReturnWithMessage(False, f"PR ID is required")
    if not result:
        return ReturnWithMessage(False, f"No validation result found for PR #{pr_id}")
    dao.save_validation_result_approval(
        result.result_id, TempConstant.APPROVER_ID, approval_result
    )
    ret = ReturnWithMessage(success=True)

    print("Sending approval comment to Azure DevOps...")
    message = f"Validation approved by {TempConstant.APPROVER_ID}"
    response = create_pr_thread_ado(repo_id, pr_id, message)
    print("Azure Devops response: ", response)

    ret_msgs = [f"Validation result PR #{pr_id} {approval_result.name}."]
    if approval_result == ApprovalResultEnum.approved:
        requeue_ret = requeue_pr_pipeline_ado(pr_id)
        ret_msgs.append(requeue_ret.message)
    ret.message = "\n".join(ret_msgs)
    return ret


def approve_cli(approval: str, pr_id: str, repo_id: str, commit_id: str) -> int:
    approval_map = {
        "approve": ApprovalResultEnum.approved,
        "reject": ApprovalResultEnum.rejected,
    }
    approval_result = approval_map.get(approval)
    ret = approve(pr_id, repo_id, approval_result, commit_id)
    print(ret.message)
    return 0 if ret.success else 1
