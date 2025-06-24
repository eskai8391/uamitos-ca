from dataclasses import dataclass
from Domain.ValueObjects import StudentUuid, Email, Phone, ZipCode, Password

@dataclass
class Student:
    id: StudentUuid
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