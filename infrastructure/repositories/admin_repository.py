from sqlalchemy.orm import Session

from domain.value_objects import Uuid, Email, Password
from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.entities.admin import Admin
from domain.entities.user import UserRole
from infrastructure.models.admin_model import AdminModel
from infrastructure.models.user_model import UserModel


class AdminRepository(BaseEntityRepository[Admin, AdminModel]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Admin | None:
        model = (
            self.__db.query(AdminModel, UserModel)
            .join(UserModel, AdminModel.uuid == UserModel.uuid)
            .filter(AdminModel.uuid == str(uuid))
            .first()
        )
        if model:
            return self._to_entity(model)
        return None

    def get_all(self) -> list[Admin]:
        models = (
            self.__db.query(AdminModel, UserModel)
            .join(UserModel, AdminModel.uuid == UserModel.uuid)
            .all()
        )
        return [self._to_entity(model) for model in models]

    def create(self, entity: Admin) -> Admin | None:
        # Create user model
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.ADMIN,
            is_active=entity.is_active,
            last_login = entity.last_login
        )
        
        # Create admin model
        admin_model = AdminModel(
            uuid=str(entity.uuid),
            access_level=entity.access_level
        )
        
        # Add to database and commit
        self.__db.add(user_model)
        self.__db.add(admin_model)
        self.__db.commit()
        
        # Refresh models
        self.__db.refresh(user_model)
        self.__db.refresh(admin_model)
        
        # Return entity
        model = (
            self.__db.query(AdminModel, UserModel)
            .join(UserModel, AdminModel.uuid == UserModel.uuid)
            .filter(AdminModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self._to_entity(model) if model else None

    def update(self, entity: Admin) -> Admin | None:
        # Get models
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(entity.uuid)).first()
        admin_model = self.__db.query(AdminModel).filter(AdminModel.uuid == str(entity.uuid)).first()
        
        if not user_model or not admin_model:
            return None
            
        # Update user model
        user_model.email = entity.email.value
        user_model.first_name = entity.first_name
        user_model.last_name = entity.last_name
        user_model.is_active = entity.is_active
        
        # Update admin model
        admin_model.access_level = entity.access_level
        
        # Commit changes
        self.__db.commit()
        self.__db.refresh(user_model)
        self.__db.refresh(admin_model)
        
        # Return entity
        model = (
            self.__db.query(AdminModel, UserModel)
            .join(UserModel, AdminModel.uuid == UserModel.uuid)
            .filter(AdminModel.uuid == str(entity.uuid))
            .first()
        )
        
        return self._to_entity(model) if model else None

    def delete(self, uuid) -> bool:
        # Get models
        admin_model = self.__db.query(AdminModel).filter(AdminModel.uuid == str(uuid)).first()
        user_model = self.__db.query(UserModel).filter(UserModel.uuid == str(uuid)).first()
        
        if not admin_model or not user_model:
            return False
        
        # Delete models
        self.__db.delete(admin_model)
        self.__db.delete(user_model)
        self.__db.commit()
        
        return True

    def _to_model(self, entity: Admin) -> tuple[AdminModel, UserModel]:
        user_model = UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=UserRole.ADMIN,
            is_active=entity.is_active
        )
        
        admin_model = AdminModel(
            uuid=str(entity.uuid),
            access_level=entity.access_level
        )
        
        return admin_model, user_model

    def _to_entity(self, model_tuple) -> Admin:
        admin_model, user_model = model_tuple
        
        return Admin(
            uuid=Uuid.from_str(user_model.uuid),
            email=Email(user_model.email),
            password=Password.from_hash(user_model.password),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=UserRole.ADMIN,
            is_active=user_model.is_active,
            access_level=admin_model.access_level,
            last_login = user_model.last_login
        )