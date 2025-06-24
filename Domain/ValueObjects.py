from dataclasses import dataclass
import re
import uuid

@dataclass(frozen=True)
class StudentUuid:
    value: uuid.UUID

    @staticmethod
    def new():
        return StudentUuid(uuid.uuid4())

    @staticmethod
    def from_str(value: str):
        return StudentUuid(uuid.UUID(value))

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.value):
            raise ValueError(f"Email inv\u00e1lido: {self.value}")


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{10}$", self.value):
            raise ValueError("El tel\u00e9fono debe tener exactamente 10 d\u00edgitos.")


@dataclass(frozen=True)
class ZipCode:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{5}$", self.value):
            raise ValueError("El c\u00f3digo postal debe tener 5 d\u00edgitos.")


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise ValueError("La contrase\u00f1a debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", self.value):
            raise ValueError("La contrase\u00f1a debe tener al menos una letra may\u00fascula.")
        if not re.search(r"[a-z]", self.value):
            raise ValueError("La contrase\u00f1a debe tener al menos una letra min\u00fascula.")
        if not re.search(r"\d", self.value):
            raise ValueError("La contrase\u00f1a debe contener al menos un n\u00famero.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.value):
            raise ValueError("La contrase\u00f1a debe contener al menos un s\u00edmbolo especial.")