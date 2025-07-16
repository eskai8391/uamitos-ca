from dataclasses import dataclass
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from domain.services.password_hasher import PasswordHasher


@dataclass(frozen=True)
class Password:
    value: str

    @classmethod
    def create(cls, plain_value: str, hasher_service: "PasswordHasher") -> "Password":
        if len(plain_value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", plain_value):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", plain_value):
            raise ValueError("La contraseña debe tener al menos una letra minúscula.")
        if not re.search(r"\d", plain_value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", plain_value):
            raise ValueError("La contraseña debe contener al menos un símbolo especial.")

        hashed = hasher_service.hash_password(plain_value)
        return cls(hashed)

    @classmethod
    def from_hash(cls, hashed_value:str) -> "Password":
        return cls(hashed_value)

    def verify_password(self, plain_value: str, hasher_service: "PasswordHasher") -> bool:
        return hasher_service.verify_password(plain_value, self.value)

    def __str__(self) -> str:
        return self.value