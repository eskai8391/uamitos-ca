from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


class GradeModel(Base):
    __tablename__ = 'grades'
    
    uuid = Column(String, primary_key=True, index=True)
    student_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)
    subject_uuid = Column(String, ForeignKey("subjects.uuid"), nullable=False)
    evaluation_name = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    comments = Column(Text, nullable=True)
    
    # Relationships
    student = relationship("UserModel", foreign_keys=[student_uuid])
    subject = relationship("SubjectModel", foreign_keys=[subject_uuid])