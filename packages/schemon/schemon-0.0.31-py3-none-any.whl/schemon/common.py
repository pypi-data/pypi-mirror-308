import logging
import yaml
from enum import Enum


class ReturnWithMessage:
    """
    A class to return with success or failure and a message.
    Attributes:
        success (bool): True if the operation was successful, False otherwise.
        msg (str): The message to return.
    """
    __slots__ = ['success', 'message']

    def __init__(self, success: bool = None, message: str = None):
        self.success = success
        self.message = message


def get_logger(name='cli', level=logging.DEBUG):
    """
    Get a logger instance with the specified name and log level.

    Args:
        name (str, optional): The name of the logger. Defaults to 'cli'.
        level (int, optional): The log level for the logger. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: The logger instance.

    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # log level for handler
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.propagate = False
    return logger


logger = get_logger()


def parse_yaml(filepath: str):
    """
    Parses a YAML file and returns the parsed content.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        dict: The parsed content of the YAML file.

    """
    parsed = None
    try:
        with open(filepath) as f:
            content = f.read()
        parsed = yaml.safe_load(content)
        parsed['_full_content'] = content
    except Exception as e:
        logger.exception('parse yaml error')
    return parsed


def get_dict_value_by_path(d: dict, path: str) -> object:
    """
    Get dict value by path like $key1 / $key2 / $key3 for complicated nested dict.

    Args:
        d: Dict that the element comes from.
        path: Path string.

    Returns:
        Element in dict by path, None if not found.
    """
    keys = path.split("/")
    node = d
    for k in keys:
        node = node.get(k.strip())
        if not node:
            return None
    return node


def generic_repr(self: object) -> str:
    """Generic repr for class"""
    show_fields = []
    for k in self.__slots__:
        if not k.startswith("_"):
            show_fields.append(f"{k}={getattr(self, k)}")
    return f"{self.__class__.__name__}({', '.join(show_fields)})"


# ====== Enums ======
class ValidationTypeEnum(Enum):
    NEW = 0
    ADDED = 1
    REMOVED = 2
    MODIFIED = 3


class ValidationResultItemStatusEnum(Enum):
    FAILED = 0
    PASSED = 1
    PASSEDWITHWARNING = 2
    PASSEDWITHNEW = 3
    INVALID = 99


class ValidationReportStatusEnum(Enum):
    FAILED = 0
    PASSED = 1
    PASSEDWITHWARNING = 2
    INVALID = 99

    @property
    def report_status_text(self):
        return {
            self.PASSED: "Passed ✅",
            self.FAILED: "Failed ❌",
            self.PASSEDWITHWARNING: "Passed with warning ⚠️",
            self.INVALID: "Invalid ❌"
        }.get(self)


class ApprovalResultEnum(Enum):
    approved = "approved"
    rejected = "rejected"


# ====== constant ======
class TempConstant:
    """will be replaced later"""
    CLI_PR_ID = "cli"
    APPROVER_ID = "testuser"
    REPO_ID = "testrepo"
    COMMIT_ID = "testcommit"
