from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Enrollment(BaseEntity):
    student_uuid: str
    subject_uuid: str
    enrollment_date: datetime
    semester: str  # e.g., "2023-1"
    status: str = "active"  # active, completed, withdrawn
    final_grade: Optional[float] = None