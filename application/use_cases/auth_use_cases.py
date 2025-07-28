from dataclasses import dataclass
from typing import Optional

from domain.entities.user import User
from domain.value_objects import Email
from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.services.password_hasher import PasswordHasher
from infrastructure.security.jwt_manager import JWTManager


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    token: str
    user_uuid: str
    email: str
    role: str
    full_name: str


class AuthUseCases:
    def __init__(
        self,
        user_repository: BaseEntityRepository,
        password_hasher: PasswordHasher
    ):
        self.__user_repository = user_repository
        self.__password_hasher = password_hasher
    
    def login(self, request: LoginRequest) -> Optional[LoginResponse]:
        """
        Authenticate a user with email and password
        
        :param request: LoginRequest with email and password
        :return: LoginResponse if successful, None otherwise
        """
        try:
            # Get user by email
            user = self.__user_repository.get_by_email(request.email)
            if not user:
                return None
                
            # Verify password
            if not user.password.verify_password(request.password, self.__password_hasher):
                return None
                
            # Generate token
            token = JWTManager.create_user_token(
                uuid=user.uuid,
                email=user.email.value,
                role=user.role
            )
            
            # Create response
            return LoginResponse(
                token=token,
                user_uuid=str(user.uuid),
                email=user.email.value,
                role=user.role.value,
                full_name=user.full_name()
            )
        except Exception:
            return None