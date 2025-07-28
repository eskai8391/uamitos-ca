from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


class EnrollmentModel(Base):
    __tablename__ = 'enrollments'
    
    uuid = Column(String, primary_key=True, index=True)
    student_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)
    subject_uuid = Column(String, ForeignKey("subjects.uuid"), nullable=False)
    enrollment_date = Column(DateTime, nullable=False)
    semester = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")
    final_grade = Column(Float, nullable=True)
    
    # Relationships
    student = relationship("UserModel", foreign_keys=[student_uuid])
    subject = relationship("SubjectModel", foreign_keys=[subject_uuid])