from schemon.domain.base import Base


class Config(Base):
    def __init__(self, env:str, type_: str, name: str, log_level: str = "DEBUG"):
        self.env = env
        self.type_ = type_
        self.log_level = log_level
        self.name = name

    def get_env(self):
        return self.env

    def get_type(self):
        return self.type_
    
    def get_log_level(self):
        return self.log_level
    
    def get_name(self):
        return self.name
    