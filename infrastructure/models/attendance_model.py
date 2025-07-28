from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


class AttendanceModel(Base):
    __tablename__ = 'attendance'
    
    uuid = Column(String, primary_key=True, index=True)
    student_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)
    subject_uuid = Column(String, ForeignKey("subjects.uuid"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)  # present, absent, late, excused
    notes = Column(Text, nullable=True)
    
    # Relationships
    student = relationship("UserModel", foreign_keys=[student_uuid])
    subject = relationship("SubjectModel", foreign_keys=[subject_uuid])