import bcrypt

from domain.services.password_hasher import PasswordHasher


class BcryptHasher(PasswordHasher):
    def hash_password(self, plain_value: str) -> str:
        return bcrypt.hashpw(plain_value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_value: str, hashed_value: str) -> bool:
        return bcrypt.checkpw(plain_value.encode('utf-8'), hashed_value.encode('utf-8'))