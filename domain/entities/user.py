from dataclasses import dataclass
from datetime import datetime

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Email, Password, Uuid
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


@dataclass
class User(BaseEntity):
    email: Email
    password: Password
    first_name: str
    last_name: str
    role: str
    is_active: bool
    last_login:  datetime

    def __post_init__(self):
        self.is_active = True
        self.last_login = datetime.now()