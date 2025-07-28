from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.db import Base
from infrastructure.models.user_model import UserModel


class TeacherModel(Base):
    __tablename__ = 'teachers'
    
    uuid = Column(String, ForeignKey("users.uuid"), primary_key=True)
    phone = Column(String)
    department = Column(String)
    specialization = Column(String)
    
    # Relationship with UserModel
    user = relationship("UserModel", backref="teacher_profile")