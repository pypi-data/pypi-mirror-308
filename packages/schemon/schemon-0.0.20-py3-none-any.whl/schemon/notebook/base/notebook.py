from typing import List
from schemon.domain.base import Base
from schemon.notebook.base.config import Config
from schemon.domain.contract.contract import Contract
from schemon_python_logger.logger import Logger
from schemon.service.contract.contract_service import load_contract_from_db_by_task_name


class Notebook(Base):

    def __init__(
        self,
        platform,
        config: Config,
        name,
    ):
        self.platform = platform
        self.config = config  # Environment configuration
        self.name = name
        self.parameters = {}  # General notebook parameters
        self.contracts: List[Contract] = (
            []
        )  # List of contracts to be used in the notebook
        self.sections = []
        self.logger = None  # Placeholder for a logger

        self.set_contracts(name)
        self.initialize_logger(config.log_level)

    def set_parameter(self, key, value):
        self.parameters[key] = value

    def set_parameters(self, parameters):
        self.parameters = parameters

    def get_parameter(self, key, default=None):
        return self.parameters.get(key, default)

    def set_contracts(self, name):
        if self.config is not None:
            self.contracts = load_contract_from_db_by_task_name(
                name, self.config.get_env()
            )            
            contract_names = [contract.entity.name for contract in self.contracts]
            print(f"CONFIG | contracts to process: {contract_names}")
        else:
            raise ValueError("Config is not set")

    def get_contracts(self):
        return self.contracts

    def set_sections(self, sections):
        self.sections = sections

    def get_sections(self):
        return self.sections

    def initialize_logger(self, log_level):
        self.logger = Logger(self.name, level=log_level)

    def get_logger(self):
        return self.logger
