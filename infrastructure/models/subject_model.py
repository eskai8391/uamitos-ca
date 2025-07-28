from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


class SubjectModel(Base):
    __tablename__ = 'subjects'
    
    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    description = Column(String)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    teacher_uuid = Column(String, ForeignKey("users.uuid"), nullable=True)