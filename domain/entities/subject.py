from dataclasses import dataclass
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Subject(BaseEntity):
    name: str
    code: str
    description: str
    credits: int
    semester: int
    teacher_uuid: Optional[str] = None