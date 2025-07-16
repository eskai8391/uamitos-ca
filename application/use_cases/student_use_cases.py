from typing import Any, Optional, List
from dataclasses import dataclass

from domain.entities.student import Student
from domain.errors.EntityNotFoundError import EntityNotFoundError
from domain.services import PasswordHasher
from domain.value_objects import Uuid, Email, Phone, ZipCode, Password
from domain.repositories.base_entity_repository import BaseEntityRepository

@dataclass
class RegisterStudentRequest:
    name: str
    last_name: str
    age: int
    email: Email
    phone: Phone
    address: str
    city: str
    state: str
    zip_code: str
    plain_password: str

@dataclass
class UpdateStudentRequest:
    uuid: str
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int]   = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str]    = None
    state: Optional[str]   = None
    zip_code: Optional[str]= None
    plain_password: Optional[str] = None

@dataclass
class DeleteStudentRequest:
    uuid: str

class StudentUseCases:
    def __init__(self, repository: BaseEntityRepository[Student, Any], password_hasher: PasswordHasher):
        self.__repository = repository
        self.__password_hasher = password_hasher

    def register_student(self, request: RegisterStudentRequest) -> Student:
        password = Password.create(request.plain_password, self.__password_hasher)

        student = Student(
            uuid        = Uuid.new(),
            name        = request.name,
            last_name   = request.last_name,
            age         = request.age,
            email       = Email(request.email),
            phone       = Phone(request.phone),
            address     = request.address,
            city        = request.city,
            state       = request.state,
            zip_code    = ZipCode(request.zip_code),
            password    = password
        )
        return self.__repository.create(student)

    def update_student(self, request: UpdateStudentRequest) -> Student:
        existing = self.__repository.get_by_uuid(request.uuid)
        if existing is None:
            raise EntityNotFoundError()

        updated_student = Student(
            uuid = Uuid.new(),
            name = request.name or existing.name,
            last_name = request.last_name or existing.last_name,
            age = request.age or existing.age,
            email = Email(request.email) if request.email else existing.email,
            phone = Phone(request.phone) if request.phone else existing.phone,
            address = request.address or existing.address,
            city = request.city or existing.city,
            state = request.state or existing.state,
            zip_code = ZipCode(request.zip_code) if request.zip_code else existing.zip_code,
            password = (Password.create(request.plain_password, self.__password_hasher)) if request.plain_password else existing.password,
        )

        return self.__repository.update(updated_student)

    def delete_student(self, request: DeleteStudentRequest) -> bool:
        existing = self.__repository.get_by_uuid(request.uuid)
        if existing is None:
            raise EntityNotFoundError()
        return self.__repository.delete(existing)

    def list_students(self) -> List[Student]:
        return self.__repository.get_all()