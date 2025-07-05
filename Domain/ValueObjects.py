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


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.value):
            raise ValueError(f"Email inválido: {self.value}")


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{10}$", self.value):
            raise ValueError("El teléfono debe tener exactamente 10 dígitos.")


@dataclass(frozen=True)
class ZipCode:
    value: str

    def __post_init__(self):
        if not re.match(r"^\d{5}$", self.value):
            raise ValueError("El código postal debe tener 5 dígitos.")


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", self.value):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", self.value):
            raise ValueError("La contraseña debe tener al menos una letra minúscula.")
        if not re.search(r"\d", self.value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.value):
            raise ValueError("La contraseña debe contener al menos un símbolo especial.")