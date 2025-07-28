import logging
from typing import Optional, Callable, Dict, Any

from application.use_cases.auth_use_cases import AuthUseCases, LoginRequest, LoginResponse
from domain.entities.user import UserRole
from infrastructure.database import SessionLocal
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security.bcrypt_hasher import BcryptHasher


class AuthController:
    """Controller for authentication related operations"""
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._session = SessionLocal()
        self._user_repository = UserRepository(self._session)
        self._password_hasher = BcryptHasher()
        self._auth_use_cases = AuthUseCases(self._user_repository, self._password_hasher)
        self._current_user: Optional[LoginResponse] = None
    
    def login(self, email: str, password: str) -> Optional[LoginResponse]:
        """
        Attempt to log in a user with the given credentials
        
        :param email: User email
        :param password: User password
        :return: LoginResponse if successful, None otherwise
        """
        try:
            self._logger.info(f"Login attempt for {email}")
            
            # Create login request
            request = LoginRequest(email=email, password=password)
            
            # Process login with use case
            response = self._auth_use_cases.login(request)
            
            if response:
                self._logger.info(f"Login successful for {email}")
                self._current_user = response
                return response
            else:
                self._logger.warning(f"Login failed for {email}")
                return None
                
        except Exception as e:
            self._logger.error(f"Error during login: {e}", exc_info=True)
            return None
    
    def get_current_user(self) -> Optional[LoginResponse]:
        """
        Get the currently logged in user
        
        :return: Current user or None if no user is logged in
        """
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated
        
        :return: True if a user is logged in, False otherwise
        """
        return self._current_user is not None
    
    def logout(self) -> None:
        """
        Log out the current user
        """
        if self._current_user:
            self._logger.info(f"User {self._current_user.email} logged out")
            self._current_user = None
    
    def get_role(self) -> Optional[str]:
        """
        Get the role of the current user
        
        :return: Role of the current user or None if no user is logged in
        """
        return self._current_user.role if self._current_user else None
    
    def is_admin(self) -> bool:
        """
        Check if the current user is an admin
        
        :return: True if the current user is an admin, False otherwise
        """
        return self.get_role() == UserRole.ADMIN.value
    
    def is_teacher(self) -> bool:
        """
        Check if the current user is a teacher
        
        :return: True if the current user is a teacher, False otherwise
        """
        return self.get_role() == UserRole.TEACHER.value
    
    def is_student(self) -> bool:
        """
        Check if the current user is a student
        
        :return: True if the current user is a student, False otherwise
        """
        return self.get_role() == UserRole.STUDENT.value
    
    def close(self) -> None:
        """
        Close the controller and its resources
        """
        if self._session:
            self._session.close()