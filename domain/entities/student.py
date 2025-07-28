from dataclasses import dataclass

from domain.entities.user import User, UserRole
from domain.value_objects import Email, Phone, ZipCode, Password, Uuid


@dataclass
class Student(User):
    age: int
    phone: Phone
    address: str
    city: str
    state: str
    zip_code: ZipCode
    
    def __post_init__(self):
        self.role = UserRole.STUDENT