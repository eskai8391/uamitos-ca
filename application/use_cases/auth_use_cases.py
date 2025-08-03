from dataclasses import dataclass
from typing import Optional

from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.services.password_hasher import PasswordHasher
from domain.entities.user import UserRole  # Agregar esta importación
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
            import logging
            logger = logging.getLogger(__name__)

            # Debug log the verification attempt
            logger.debug(f"Verifying password for user: {user.email.value}")
            logger.debug(f"Stored password hash: {str(user.password)[:10]}...")
            
            verification_result = user.password.verify_password(request.password, self.__password_hasher)
            logger.debug(f"Password verification result: {verification_result}")
            
            if not verification_result:
                return None
                
            # Generate token - Asegurar que role sea del tipo correcto
            user_role = user.role if isinstance(user.role, UserRole) else UserRole(user.role)
            logger.debug(f"User role type: {type(user_role)}, value: {user_role}")
            
            token = JWTManager.create_user_token(
                uuid=user.uuid,
                email=user.email.value,
                role=user_role
            )
            
            # Create response
            return LoginResponse(
                token=token,
                user_uuid=str(user.uuid),
                email=user.email.value,
                role=user.role.value if hasattr(user.role, 'value') else str(user.role),
                full_name=f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else ""
            )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return None