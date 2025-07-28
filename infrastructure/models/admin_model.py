from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.db import Base
from infrastructure.models.user_model import UserModel


class AdminModel(Base):
    __tablename__ = 'admins'
    
    uuid = Column(String, ForeignKey("users.uuid"), primary_key=True)
    access_level = Column(Integer, default=1)
    
    # Relationship with UserModel
    user = relationship("UserModel", backref="admin_profile")