from sqlalchemy import Column, String, Integer, ForeignKey, Time, Table
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


# Association table for many-to-many relationship between groups and students
group_students = Table(
    'group_students', 
    Base.metadata,
    Column('group_uuid', String, ForeignKey('groups.uuid')),
    Column('student_uuid', String, ForeignKey('users.uuid'))
)


class GroupModel(Base):
    __tablename__ = 'groups'
    
    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject_uuid = Column(String, ForeignKey("subjects.uuid"), nullable=False)
    teacher_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 1=Tuesday, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String, nullable=False)
    max_students = Column(Integer, nullable=False, default=30)
    semester = Column(String, nullable=False, default="current")
    
    # Relationships
    subject = relationship("SubjectModel", foreign_keys=[subject_uuid])
    teacher = relationship("UserModel", foreign_keys=[teacher_uuid])
    
    # Many-to-many relationship with students
    students = relationship(
        "UserModel",
        secondary=group_students,
        primaryjoin="GroupModel.uuid == group_students.c.group_uuid",
        secondaryjoin="UserModel.uuid == group_students.c.student_uuid",
        backref="enrolled_groups"
    )