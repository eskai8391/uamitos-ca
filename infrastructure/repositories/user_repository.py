from sqlalchemy.orm import Session

from domain.value_objects import Uuid, Email, Password
from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.entities.user import User, UserRole
from infrastructure.models.user_model import UserModel


class UserRepository(BaseEntityRepository[User, UserModel]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> User | None:
        model = self.__db.query(UserModel).filter(UserModel.uuid == str(uuid)).first()
        if model:
            return self._to_entity(model)
        return None
    
    def get_by_email(self, email: str) -> User | None:
        model = self.__db.query(UserModel).filter(UserModel.email == email).first()
        if model:
            return self._to_entity(model)
        return None

    def get_all(self) -> list[User]:
        models = self.__db.query(UserModel).all()
        return [self._to_entity(model) for model in models]

    def create(self, entity: User) -> User | None:
        model = self._to_model(entity)
        self.__db.add(model)
        self.__db.commit()
        self.__db.refresh(model)
        return self._to_entity(model)

    def update(self, entity: User) -> User | None:
        model = self.__db.query(UserModel).filter(UserModel.uuid == str(entity.uuid)).first()
        if not model:
            return None
            
        # Update model properties
        model.email = entity.email.value
        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.role = entity.role
        model.is_active = entity.is_active
        
        self.__db.commit()
        self.__db.refresh(model)
        return self._to_entity(model)

    def delete(self, uuid) -> bool:
        model = self.__db.query(UserModel).filter(UserModel.uuid == str(uuid)).first()
        if not model:
            return False
        
        self.__db.delete(model)
        self.__db.commit()
        return True

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            uuid=str(entity.uuid),
            email=entity.email.value,
            password=entity.password.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=entity.role,
            is_active=entity.is_active,
            last_login=entity.last_login
        )

    def _to_entity(self, model: UserModel) -> User:
        return User(
            uuid=Uuid.from_str(model.uuid),
            email=Email(model.email),
            password=Password.from_hash(model.password),
            first_name=model.first_name,
            last_name=model.last_name,
            role=model.role,
            is_active=model.is_active,
            last_login = model.last_login
        )