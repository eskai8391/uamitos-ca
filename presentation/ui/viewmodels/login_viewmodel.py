import logging
from typing import Optional, Callable

from PySide6.QtCore import QObject, Signal, Slot, Property

from presentation.controllers.auth_controller import AuthController


class LoginViewModel(QObject):
    """View model for the login screen"""
    
    # Signals
    loginSuccessful = Signal(str, str, str)  # user_uuid, role, full_name
    loginFailed = Signal(str)  # error_message
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._auth_controller = AuthController()
        
        # Properties
        self._email = ""
        self._password = ""
        self._is_logging_in = False
        self._error_message = ""
    
    @Property(str)
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if self._email != value:
            self._email = value
            print(f"Email updated: {value}")
    
    @Property(str)
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, value: str) -> None:
        if self._password != value:
            self._password = value
            print(f"Password updated (length: {len(value)})")
    
    @Property(bool)
    def is_logging_in(self) -> bool:
        return self._is_logging_in
    
    @Property(str)
    def error_message(self) -> str:
        return self._error_message
    
    @Slot()
    def login(self) -> None:
        """
        Attempt to log in with the current email and password
        """
        try:
            print(f"Login attempt with email: {self._email}")
            self._logger.info(f"Attempting login for: {self._email}")
            self._is_logging_in = True
            self._error_message = ""
            
            # Validate inputs
            if not self._email:
                self._error_message = "Por favor ingrese su correo electrónico"
                self._is_logging_in = False
                print(f"Login error: {self._error_message}")
                self.loginFailed.emit(self._error_message)
                return
                
            if not self._password:
                self._error_message = "Por favor ingrese su contraseña"
                self._is_logging_in = False
                print(f"Login error: {self._error_message}")
                self.loginFailed.emit(self._error_message)
                return
            
            # For testing/debugging - simulate successful login with test credentials
            if self._email == "test@test.com" and self._password == "test123":
                print("Debug login successful with test credentials")
                self.loginSuccessful.emit(
                    "test-uuid-123",
                    "admin",
                    "Test User"
                )
                return
            
            # Attempt login through controller
            response = self._auth_controller.login(self._email, self._password)
            
            if response:
                print(f"Login successful for: {self._email}, role: {response.role}")
                self._logger.info(f"Login successful for: {self._email}")
                self.loginSuccessful.emit(
                    response.user_uuid,
                    response.role,
                    response.full_name
                )
            else:
                self._error_message = "Correo o contraseña incorrectos"
                print(f"Login failed: {self._error_message}")
                self.loginFailed.emit(self._error_message)
                
        except Exception as e:
            self._logger.error(f"Error during login: {e}", exc_info=True)
            print(f"Login exception: {str(e)}")
            self._error_message = f"Error al intentar iniciar sesión: {str(e)}"
            self.loginFailed.emit(self._error_message)
        finally:
            self._is_logging_in = False
    
    @Slot()
    def clear_inputs(self) -> None:
        """
        Clear the email and password inputs
        """
        self._email = ""
        self._password = ""
        self._error_message = ""
        print("Login inputs cleared")
    
    def dispose(self) -> None:
        """
        Clean up resources
        """
        if self._auth_controller:
            self._auth_controller.close()