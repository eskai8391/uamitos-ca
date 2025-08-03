from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects import Uuid


@dataclass
class Event(BaseEntity):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    organizer_uuid: str  # UUID of teacher or admin who organized the event
    event_type: str  # class, meeting, excursion, etc.
    all_day: bool = False
    max_participants: Optional[int] = None