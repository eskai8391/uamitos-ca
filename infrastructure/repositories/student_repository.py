from abc import ABC

from sqlalchemy.orm import Session

from domain.value_objects import Uuid, ZipCode, Phone, Email, Password
from domain.repositories.base_entity_repository import BaseEntityRepository, M, E
from domain.entities.student import Student
from domain.entities.user import UserRole
from infrastructure.models.student_model import StudentModel
from infrastructure.models.user_model import UserModel


class StudentRepository(BaseEntityRepository[Student, StudentModel]):
    def _to_entity(self, model: M) -> E:
        pass

    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Student | None:
        # Join student and user models
        result = (
            self.__db.query(StudentModel, UserModel)
            .join(UserModel, StudentModel.uuid == UserModel.uuid)
            .filter(StudentModel.uuid == str(uuid))
            .first()
        )
        
        if result:
            return self.__to_entity(result)
        return None

    def get_all(self) -> list[Student]:
        results = (
            self.__db.query(StudentModel, UserModel)
            .join(UserModel, StudentModel.uuid == UserModel.uuid)
            .all()
        )
        return [self.__to_entity(result) for result in results]

    def create(self, entity: Student) -> Student | None:
        # Create user model
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.STUDENT,
            is_active=entity.is_active,
            last_login = entity.last_login
        )
        
        # Create student model
        student_model = StudentModel(
            uuid=str(entity.uuid),
            phone=entity.phone.value,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code.value,
            age=entity.age
        )
        
        # Add to database and commit
        self.__db.add(user_model)
        self.__db.add(student_model)
        self.__db.commit()
        
        # Refresh models
        self.__db.refresh(user_model)
        self.__db.refresh(student_model)
        
        # Return entity
        result = (
            self.__db.query(StudentModel, UserModel)
            .join(UserModel, StudentModel.uuid == UserModel.uuid)
            .filter(StudentModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self.__to_entity(result) if result else None

    def update(self, entity: Student) -> Student | None:
        # Get models
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(entity.uuid)).first()
        student_model = self.__db.query(StudentModel).filter(StudentModel.uuid == str(entity.uuid)).first()
        
        if not user_model or not student_model:
            return None
            
        # Update user model
        user_model.email = entity.email.value
        user_model.first_name = entity.first_name
        user_model.last_name = entity.last_name
        user_model.is_active = entity.is_active
        
        # Update student model
        student_model.phone = entity.phone.value
        student_model.address = entity.address
        student_model.city = entity.city
        student_model.state = entity.state
        student_model.zip_code = entity.zip_code.value
        student_model.age = entity.age
        
        # Commit changes
        self.__db.commit()
        self.__db.refresh(user_model)
        self.__db.refresh(student_model)
        
        # Return entity
        result = (
            self.__db.query(StudentModel, UserModel)
            .join(UserModel, StudentModel.uuid == UserModel.uuid)
            .filter(StudentModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self.__to_entity(result) if result else None

    def delete(self, uuid) -> bool:
        # Get models
        student_model = self.__db.query(StudentModel).filter(StudentModel.uuid == str(uuid)).first()
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(uuid)).first()
        
        if not student_model or not user_model:
            return False
        
        # Delete models
        self.__db.delete(student_model)
        self.__db.delete(user_model)
        self.__db.commit()
        
        return True

    def _to_model(self, entity: Student) -> tuple[StudentModel, UserModel]:
        """Convert entity to models"""
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.STUDENT,
            is_active=entity.is_active,
            last_login = entity.last_login
        )
        
        student_model = StudentModel(
            uuid=str(entity.uuid),
            phone=entity.phone.value,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code.value,
            age=entity.age
        )
        
        return (student_model, user_model)

    def __to_entity(self, result) -> Student:
        """Convert joined query result to entity"""
        student_model, user_model = result
        
        return Student(
            uuid=Uuid.from_str(user_model.uuid),
            email=Email(user_model.email),
            password=Password.from_hash(user_model.password),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=UserRole.STUDENT,
            is_active=user_model.is_active,
            phone=Phone(student_model.phone),
            address=student_model.address,
            city=student_model.city,
            state=student_model.state,
            zip_code=ZipCode(student_model.zip_code),
            age=student_model.age,
            last_login = user_model.last_login
        )