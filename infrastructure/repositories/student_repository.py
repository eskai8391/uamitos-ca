from abc import ABC

from sqlalchemy.orm import Session

from domain.value_objects import Uuid, ZipCode, Phone, Email, Password
from domain.repositories.base_entity_repository import IBaseEntityRepository, M, E
from domain.entities.student import Student
from infrastructure.models.student_model import StudentModel


class StudentRepository(IBaseEntityRepository[Student, StudentModel]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Student | None:
        model = self.__db.query(StudentModel).filter(StudentModel.uuid == str(uuid)).first()
        if model:
            return self.__to_entity(model)
        return None

    def get_all(self) -> list[Student]:
        models = self.__db.query(StudentModel).all()
        return [self.__to_entity(model) for model in models]

    def create(self, entity: Student) -> Student | None:
        model = self.__to_model(entity)
        self.__db.add(model)
        self.__db.commit()
        self.__db.refresh(model)
        return self.__to_entity(model)

    def update(self, uuid) -> Student | None:
        pass

    def delete(self, uuid) -> bool:
        pass

    def __to_model(self, entity: Student) -> StudentModel | None:
        return StudentModel(
            uuid=str(entity.uuid),
            name=entity.name,
            last_name=entity.last_name,
            age=entity.age,
            email=entity.email.value,
            password=entity.password,
            phone=entity.phone.value,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code.value,
        )


    def __to_entity(self, model: StudentModel) -> Student:
        return Student(
            uuid=Uuid.from_str(model.uuid),
            name=model.name,
            last_name=model.last_name,
            age=model.age,
            email=Email(model.email),
            password=Password(model.password),
            phone=Phone(model.phone),
            address=model.address,
            city=model.city,
            state=model.state,
            zip_code=ZipCode(model.zip_code)
        )