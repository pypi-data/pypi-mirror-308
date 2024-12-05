from schemon.domain.contract import Entity


def load_entity(data: dict) -> Entity:
    name = data.get("name")
    description = data.get("description")
    return Entity(name=name, description=description)
