from sqlalchemy import Column, String, Boolean, Enum, DateTime
from infrastructure.database.db import Base
from domain.entities.user import UserRole


class UserModel(Base):
    __tablename__ = 'users'
    
    uuid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=False)