import re
from collections import defaultdict


def replace_handle_tokens(text: str, token_values: dict = {}):
    """
    Replace tokens in the format @type(token) in the text with values from the token_values dictionary.

    Args:
    - text (str): The string containing the tokens to be replaced.
    - token_values (dict): A dictionary where each key is a token type (e.g., 'env', 'config')
                           and each value is a dictionary mapping tokens to replacement values.
                           Example: {'env': {'location': 'NYC', 'database': 'global_dev'}}

    Returns:
    - str: The updated string with tokens replaced.

    Example:
    >>> text = "SELECT * FROM @env(location) WHERE db = @env(database)"
    >>> token_values = {"env": {"location": "NYC", "database": "global_dev"}}
    >>> replace_handle_tokens(text, token_values)
    "SELECT * FROM NYC WHERE db = global_dev"
    """
    for token_type, values in token_values.items():
        for token, value in values.items():
            text = re.sub(rf"@{token_type}\({token}\)", str(value), text)
    return text


def extract_handle_tokens(text: str):
    """
    Extract all occurrences of @handle(token) patterns from the text and return them as a dictionary,
    where each handle maps to a set of unique tokens.

    Args:
    - text (str): The string containing the @handle(token) patterns.

    Returns:
    - dict: A dictionary where each handle is a key and each value is a set of tokens.

    Example:
    >>> text = "SELECT * FROM @env(location) AND @config(database)"
    >>> extract_handle_tokens(text)
    {"env": {"location"}, "config": {"database"}}
    """
    # Regular expression to match @handle(token)
    pattern = r"@(\w+)\(([^)]+)\)"

    # Dictionary to store handles and their associated tokens
    result = defaultdict(set)

    # Find all matches and populate the dictionary
    for handle, token in re.findall(pattern, text):
        result[handle].add(token)

    return dict(result)
