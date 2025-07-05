from abc import ABC

from sqlalchemy.orm import Session

from Domain.Repositories.IBaseEntityRepository import IBaseEntityRepository, E
from Domain.Entities.Student import Student
from Infraestructure.Models.StudentModel import StudentModel


class StudentRepository(IBaseEntityRepository[Student]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Student | None:
        model = self.__db.query(StudentModel).filter(StudentModel.uuid == str(uuid)).first()
        if model:
            return self._model_to_entity(model)
        return None


    def _model_to_entity(self, model: StudentModel) -> Student:
        return Student(
            uuid=model.uuid,
            name=model.name,
            last_name=model.last_name,
            age=model.age,
            email=model.email,
            password=model.password,
            phone=model.phone,
            address=model.address,
            city=model.city,
            state=model.state,
            zip_code=model.zip_code,
        )
