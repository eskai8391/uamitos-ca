from dataclasses import dataclass

from Domain.Entities.BaseEntity import BaseEntity
from Domain.ValueObjects import Email, Phone, ZipCode, Password

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