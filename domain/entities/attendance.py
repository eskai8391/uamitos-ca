from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Attendance(BaseEntity):
    student_uuid: str
    subject_uuid: str
    date: datetime
    status: str  # present, absent, late, excused
    notes: Optional[str] = ""