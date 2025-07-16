from sqlalchemy import Column, Integer, String
from infrastructure.database.db import Base

class StudentModel(Base):
    __tablename__ = 'student'
    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    password = Column(String)
