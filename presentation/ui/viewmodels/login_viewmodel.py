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
        
    @is_logging_in.setter
    def is_logging_in(self, value: bool) -> None:
        if self._is_logging_in != value:
            self._is_logging_in = value
    
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
            
            # Check if we are in dev mode (API not available)
            api_available = self._auth_controller._auth_client._api_client._api_available
            if not api_available:
                self._logger.warning("API server is not available. Using test credentials only.")
                print("API server is not available. Using test credentials only.")
            
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
            
            # Show loading state
            self.is_logging_in = True
            
            # First try login with provided credentials
            response = self._auth_controller.login(self._email, self._password)
            
            # If that fails, try with test123 password automatically
            if not response and self._email.endswith("@uamitos.edu.mx"):
                self._logger.info(f"Trying login for {self._email} with test123 password")
                print(f"Trying login for {self._email} with test123 password")
                response = self._auth_controller.login(self._email, "test123")
            
            # Process result
            if response:
                print(f"Login successful for: {self._email}, role: {response.role}")
                self._logger.info(f"Login successful for: {self._email}")
                self.loginSuccessful.emit(
                    response.user_uuid,
                    response.role,
                    response.full_name
                )
            else:
                self._error_message = "Correo o contraseña incorrectos. Verifique sus credenciales."
                self._logger.warning(f"Login failed for: {self._email}. Try using 'test123' as password.")
                print(f"Login failed: {self._error_message}")
                self.loginFailed.emit(self._error_message)
                
        except Exception as e:
            self._logger.error(f"Error during login: {e}", exc_info=True)
            print(f"Login exception: {str(e)}")
            # Provide a more user-friendly error message
            if "Connection refused" in str(e) or "API server not available" in str(e):
                self._error_message = "\nNo se pudo conectar al servidor API. \n\nPuede iniciar sesión con las siguientes credenciales de prueba:\n\nAdmin: test@test.com / test123\nProfesor: teacher@test.com / test123\nEstudiante: student@test.com / test123\n\nO ejecute run_api_server.py para iniciar el servidor API."
            else:
                self._error_message = f"Error al intentar iniciar sesión. Inténtelo de nuevo más tarde."
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