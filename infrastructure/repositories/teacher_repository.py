from sqlalchemy.orm import Session

from domain.value_objects import Uuid, Email, Phone, Password
from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.entities.teacher import Teacher
from domain.entities.user import UserRole
from infrastructure.models.teacher_model import TeacherModel
from infrastructure.models.user_model import UserModel


class TeacherRepository(BaseEntityRepository[Teacher, TeacherModel]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Teacher | None:
        model = (
            self.__db.query(TeacherModel, UserModel)
            .join(UserModel, TeacherModel.uuid == UserModel.uuid)
            .filter(TeacherModel.uuid == str(uuid))
            .first()
        )
        if model:
            return self._to_entity(model)
        return None

    def get_all(self) -> list[Teacher]:
        models = (
            self.__db.query(TeacherModel, UserModel)
            .join(UserModel, TeacherModel.uuid == UserModel.uuid)
            .all()
        )
        return [self._to_entity(model) for model in models]

    def create(self, entity: Teacher) -> Teacher | None:
        # Create user model
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.TEACHER,
            is_active=entity.is_active,
            last_login = entity.last_login
        )
        
        # Create teacher model
        teacher_model = TeacherModel(
            uuid=str(entity.uuid),
            phone=entity.phone.value,
            department=entity.department,
            specialization=entity.specialization
        )
        
        # Add to database and commit
        self.__db.add(user_model)
        self.__db.add(teacher_model)
        self.__db.commit()
        
        # Refresh models
        self.__db.refresh(user_model)
        self.__db.refresh(teacher_model)
        
        # Return entity
        model = (
            self.__db.query(TeacherModel, UserModel)
            .join(UserModel, TeacherModel.uuid == UserModel.uuid)
            .filter(TeacherModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self._to_entity(model) if model else None

    def update(self, entity: Teacher) -> Teacher | None:
        # Get models
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(entity.uuid)).first()
        teacher_model = self.__db.query(TeacherModel).filter(TeacherModel.uuid == str(entity.uuid)).first()
        
        if not user_model or not teacher_model:
            return None
            
        # Update user model
        user_model.email = entity.email.value
        user_model.first_name = entity.first_name
        user_model.last_name = entity.last_name
        user_model.is_active = entity.is_active
        
        # Update teacher model
        teacher_model.phone = entity.phone.value
        teacher_model.department = entity.department
        teacher_model.specialization = entity.specialization
        
        # Commit changes
        self.__db.commit()
        self.__db.refresh(user_model)
        self.__db.refresh(teacher_model)
        
        # Return entity
        model = (
            self.__db.query(TeacherModel, UserModel)
            .join(UserModel, TeacherModel.uuid == UserModel.uuid)
            .filter(TeacherModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self._to_entity(model) if model else None

    def delete(self, uuid) -> bool:
        # Get models
        teacher_model = self.__db.query(TeacherModel).filter(TeacherModel.uuid == str(uuid)).first()
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(uuid)).first()
        
        if not teacher_model or not user_model:
            return False
        
        # Delete models
        self.__db.delete(teacher_model)
        self.__db.delete(user_model)
        self.__db.commit()
        
        return True

    def _to_model(self, entity: Teacher) -> tuple[TeacherModel, UserModel]:
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.TEACHER,
            is_active=entity.is_active,
            last_login = entity.last_login
        )
        
        teacher_model = TeacherModel(
            uuid=str(entity.uuid),
            phone=entity.phone.value,
            department=entity.department,
            specialization=entity.specialization
        )
        
        return teacher_model, user_model

    def _to_entity(self, model_tuple) -> Teacher:
        teacher_model, user_model = model_tuple
        
        return Teacher(
            uuid=Uuid.from_str(user_model.uuid),
            email=Email(user_model.email),
            password=Password.from_hash(user_model.password),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=UserRole.TEACHER,
            is_active=user_model.is_active,
            phone=Phone(teacher_model.phone),
            department=teacher_model.department,
            specialization=teacher_model.specialization,
            last_login = user_model.last_login
        )