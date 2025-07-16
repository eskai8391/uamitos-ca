from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{10}$", self.value):
            raise ValueError("El teléfono debe tener exactamente 10 dígitos.")