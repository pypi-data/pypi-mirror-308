from schemon.domain.base import Base


class Owner(Base):
    def __init__(self, name: str, email: str):
        if not name:
            raise ValueError("Owner name is required.")
        if not email:
            raise ValueError("Owner email is required.")
        
        self.name = name
        self.email = email
