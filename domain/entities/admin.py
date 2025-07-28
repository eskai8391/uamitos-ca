from dataclasses import dataclass

from domain.entities.user import User, UserRole
from domain.value_objects import Email, Password, Uuid


@dataclass
class Admin(User):
    access_level: int = 1  # Default access level
    
    def __post_init__(self):
        # Ensure role is always ADMIN
        self.role = UserRole.ADMIN