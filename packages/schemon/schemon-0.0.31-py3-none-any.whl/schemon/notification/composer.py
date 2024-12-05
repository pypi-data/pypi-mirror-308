from __future__ import annotations
import os
from schemon.common import (
    ValidationResultItemStatusEnum,
    ValidationReportStatusEnum,
)


def get_report_status(items: list[dict]) -> ValidationReportStatusEnum:
    if all(item["status"] == ValidationReportStatusEnum.PASSED for item in items):
        status = ValidationReportStatusEnum.PASSED
    elif any(item["status"] == ValidationReportStatusEnum.FAILED for item in items):
        status = ValidationReportStatusEnum.FAILED
    elif any(
        item["status"] == ValidationReportStatusEnum.PASSEDWITHWARNING for item in items
    ):
        status = ValidationReportStatusEnum.PASSEDWITHWARNING
    else:
        raise NotImplementedError("Unknown status")  # should not be here
    return status


def generate_validation_report(items: list[dict], newline: str) -> str:
    """
    Generate a validation report based on the provided items.

    Args:
        items (list[dict]): A list of dictionaries representing the validation items.
        newline (str): The newline character to use in the report. ADO supports \n, while GitLab supports [space][space][space]\n.

    Returns:
        str: The generated validation report.

    """
    report = f"## Validation Report{newline}{newline}"
    if os.getenv("OVERRIDE_VALIDATION") == "1":
        report += f"### Overrided Validation{newline}"

    # Determine the overall status
    status_enum = get_report_status(items)
    status = status_enum.report_status_text

    report += f"### Status: {status}{newline}"
    report += f"---{newline}"
    report += f"### Details{newline}"

    for item in items:
        entity_name = item["entity"]
        status = item["status"]
        curr_version = item["curr_version"]
        new_version = item["new_version"]
        result_items = item["result"]

        report += f"- **`{entity_name}`**{newline}"
        if not result_items:
            report += f"\t✅ All good! No version change.{newline}"

        if (
            status == ValidationReportStatusEnum.PASSEDWITHWARNING
            or status == ValidationReportStatusEnum.FAILED
        ):
            report += f"\t⬆️ Version will be changed from **{curr_version}** to **{new_version}**{newline}"

        for result_item in result_items:
            if result_item.status == ValidationResultItemStatusEnum.PASSED:
                report += f"\t✅ All good! No version change.{newline}"
            elif result_item.status == ValidationResultItemStatusEnum.PASSEDWITHNEW:
                report += f"\t🆕 New entity.{newline}"
            elif result_item.status == ValidationResultItemStatusEnum.PASSEDWITHWARNING:
                report += f"\t⚠️ A {result_item.type} **{result_item.name}** is **{result_item.validation_type.name.lower()}** with message - {result_item.message}{newline}"
            elif result_item.status == ValidationResultItemStatusEnum.FAILED:
                report += f"\t❌ A {result_item.type} **{result_item.name}** is **{result_item.validation_type.name.lower()}** with message - {result_item.message}{newline}"

        report += f"{newline}"

    print(report)

    return report
