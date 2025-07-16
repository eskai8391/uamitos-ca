from abc import ABC
from dataclasses import dataclass

from domain.value_objects import Uuid

@dataclass
class BaseEntity(ABC):
    uuid: Uuid
