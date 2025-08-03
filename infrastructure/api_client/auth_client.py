import logging
from typing import Optional, Dict, Any

from application.use_cases.auth_use_cases import LoginResponse
from infrastructure.api_client.api_client import ApiClient, ApiClientException


class AuthClient:
    """Client for authentication related API operations"""
    
    def __init__(self, api_client: Optional[ApiClient] = None):
        """
        Initialize the auth client
        
        :param api_client: API client instance, creates a new one if not provided
        """
        self._logger = logging.getLogger(__name__)
        self._api_client = api_client or ApiClient()
    
    def login(self, email: str, password: str) -> Optional[LoginResponse]:
        """
        Authenticate a user with email and password via API
        
        :param email: User email
        :param password: User password
        :return: LoginResponse if successful, None otherwise
        """
        try:
            # Handle standard authentication for production
            if self._api_client._api_available:
                try:
                    # API uses OAuth2 with username field for email
                    form_data = {
                        "username": email,
                        "password": password
                    }
                    
                    response = self._api_client.post_form("login", form_data)
                    
                    # Convert API response to LoginResponse
                    login_response = LoginResponse(
                        token=response.get("token", ""),
                        user_uuid=response.get("user_uuid", ""),
                        email=response.get("email", ""),
                        role=response.get("role", ""),
                        full_name=response.get("full_name", "")
                    )
                    
                    # Store token for future API requests
                    self._api_client.set_token(login_response.token)
                    self._logger.info(f"Token set in AuthClient on ApiClient instance: {id(self._api_client)}")
                    return login_response
                except ApiClientException:
                    return None
            
            return None
                
        except Exception:
            return None
    
    def logout(self) -> bool:
        """
        Log out the current user
        
        :return: True if successful, False otherwise
        """
        # Just clear the token since there's likely no logout endpoint
        self._api_client.clear_token()
        return True
    
    def close(self) -> None:
        """Clean up resources"""
        # Nothing to clean up for now
        pass