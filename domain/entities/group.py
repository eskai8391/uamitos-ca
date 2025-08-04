from dataclasses import dataclass
from typing import Optional, List
from datetime import time

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Group(BaseEntity):
    """
    Represents a class group that has:
    - One subject
    - One teacher assigned to it
    - Multiple students (up to 30)
    - Specific schedule (day, time, room)
    """
    name: str
    subject_uuid: str
    teacher_uuid: str
    day_of_week: int  # 0=Monday, 1=Tuesday, etc.
    start_time: time
    end_time: time
    room: str
    max_students: int = 30
    semester: str = "current"
    
    # These would be populated by the repository layer
    students_uuids: List[str] = None
    
    def __post_init__(self):
        if self.students_uuids is None:
            self.students_uuids = []
        
    def add_student(self, student_uuid: str) -> bool:
        """
        Add a student to the group if not already at capacity
        
        :param student_uuid: UUID of the student to add
        :return: True if added, False if group is at capacity
        """
        if len(self.students_uuids) >= self.max_students:
            return False
            
        if student_uuid not in self.students_uuids:
            self.students_uuids.append(student_uuid)
            
        return True
        
    def remove_student(self, student_uuid: str) -> bool:
        """
        Remove a student from the group
        
        :param student_uuid: UUID of the student to remove
        :return: True if removed, False if not found
        """
        if student_uuid in self.students_uuids:
            self.students_uuids.remove(student_uuid)
            return True
        return False
        
    def is_student_in_group(self, student_uuid: str) -> bool:
        """
        Check if a student is in this group
        
        :param student_uuid: UUID of the student to check
        :return: True if student is in group
        """
        return student_uuid in self.students_uuids