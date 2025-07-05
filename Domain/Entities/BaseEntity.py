from abc import ABC
from dataclasses import dataclass

from Domain.ValueObjects import Uuid

@dataclass
class BaseEntity(ABC):
    uuid: Uuid