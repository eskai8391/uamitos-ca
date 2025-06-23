from dataclasses import dataclass
from Domain.ValueObjects import StudentUuid

@dataclass
class Student:
    id: StudentUuid
    name: str
    last_name: str
    age: int
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
