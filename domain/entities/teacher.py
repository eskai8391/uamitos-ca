from dataclasses import dataclass

from domain.entities.user import User, UserRole
from domain.value_objects import Email, Phone, Password, Uuid


@dataclass
class Teacher(User):
    phone: Phone
    department: str
    specialization: str

    def __post_init__(self):
        # Ensure role is always TEACHER
        self.role = UserRole.TEACHER