from typing import Optional
from schemon.domain.contract import Expectation, Rule


def load_expectations(data: Optional[dict]) -> Optional[Expectation]:
    """
    Loads the expectations from a dictionary (parsed from YAML).

    Args:
        data (dict or None): The parsed YAML data for expectations.

    Returns:
        Expectation or None: Returns an Expectation object if data is provided, or None if expectations is null.

    Raises:
        ValueError: If the expectations are not null, the platform or rules are missing or invalid.
    """
    if data is None:
        return None

    platform = data.get("platform")
    if platform is None:
        raise ValueError("The 'platform' must be set when expectations are not null.")

    rules_data = data.get("rules", [])
    if not rules_data:
        raise ValueError(
            "At least one rule must be provided when expectations are not null."
        )

    rules = []
    for rule_data in rules_data:
        rule = rule_data.get("rule")
        action = rule_data.get("action")
        description = rule_data.get("description", None)

        rules.append(Rule(rule=rule, action=action, description=description))

    return Expectation(platform=platform, rules=rules)
