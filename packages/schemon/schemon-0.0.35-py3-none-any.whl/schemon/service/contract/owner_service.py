from schemon.domain.contract import Owner


def load_owner(data: dict) -> Owner:
    name = data.get("name")
    email = data.get("email")
    return Owner(name=name, email=email)
