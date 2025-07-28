from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.db import Base


class StudentModel(Base):
    __tablename__ = 'students'
    
    uuid = Column(String, ForeignKey("users.uuid"), primary_key=True)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    age = Column(Integer)
    
    # Relationship with UserModel
    user = relationship("UserModel", backref="student_profile")