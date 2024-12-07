from schemon.domain.base import Base


class TypeMapping(Base):
    def __init__(self):
        self.type_mapping = {}

    def get_target_type(self, type: str):
        return self.type_mapping.get(type, "Unknown")

    def add_custom_mapping(self, pandas_type, target_type):
        """Allows adding a custom mapping from Pandas type to target platform type."""
        self.type_mapping[pandas_type] = target_type

    def remove_mapping(self, pandas_type):
        """Allows removing a type mapping."""
        if pandas_type in self.type_mapping:
            del self.type_mapping[pandas_type]

    def list_mappings(self):
        """Lists all current Pandas to target platform type mappings."""
        return self.type_mapping
