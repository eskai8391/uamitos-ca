from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ZipCode:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{5}$", self.value):
            raise ValueError("El código postal debe tener 5 dígitos.")