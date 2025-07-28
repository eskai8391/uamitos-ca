from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Grade(BaseEntity):
    student_uuid: str
    subject_uuid: str
    evaluation_name: str  # e.g., "Midterm", "Final", "Project 1"
    score: float  # Typically 0-100 or 0-10 depending on grading system
    weight: float  # Percentage weight of this grade (0-100)
    date: datetime
    comments: Optional[str] = ""