from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Email, Phone, ZipCode, Password

@dataclass
class Student(BaseEntity):
    name: str
    last_name: str
    age: int
    email: Email
    phone: Phone
    address: str
    city: str
    state: str
    zip_code: ZipCode
    password: Password