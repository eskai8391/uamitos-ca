from dataclasses import dataclass
import re
import uuid

@dataclass(frozen=True)
class Uuid:
    value: uuid.UUID

    @staticmethod
    def new():
        return Uuid(uuid.uuid4())

    @staticmethod
    def from_str(value: str):
        return Uuid(uuid.UUID(value))

    def __str__(self):
        return str(self.value)