import logging
import requests
from typing import Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')


class ApiClientException(Exception):
    """Exception raised for errors in API client operations."""
    pass


class ApiClient:
    """Base client for making HTTP requests to the API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API client
        
        :param base_url: Base URL of the API
        """
        self._base_url = base_url.rstrip("/")  # Remove trailing slash if present
        self._logger = logging.getLogger(__name__)
        self._token: Optional[str] = None
        self._api_available = self._check_api_available()
        
    def _check_api_available(self) -> bool:
        """
        Check if the API server is available
        
        :return: True if the API server is available, False otherwise
        """
        try:
            response = requests.get(f"{self._base_url}/docs", timeout=1)
            return response.status_code < 500  # Accept any response that's not a server error
        except requests.exceptions.RequestException:
            self._logger.warning("API server not available. Using fallback authentication.")
            return False
    
    def set_token(self, token: str) -> None:
        """
        Set authentication token for subsequent requests
        
        :param token: JWT token
        """
        self._token = token
        self._logger.info(f"API token set: {token[:10]}... (token length: {len(token)})")
    
    def clear_token(self) -> None:
        """Clear authentication token"""
        self._token = None
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for requests

        :return: Headers dictionary with auth token if available
        """
        headers: Dict[str, str] = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
            self._logger.debug(f"Adding auth header with token: {self._token[:10]}...")
        else:
            self._logger.warning("No token available for request, auth header not set")
        return headers
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to API
        
        :param endpoint: API endpoint (without base URL)
        :param params: Query parameters
        :return: Response data
        :raises ApiClientException: On request failure
        """
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        try:
            self._logger.info(f"Making GET request to {url}")
            response = requests.get(
                url,
                params=params,
                headers=self.get_auth_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._logger.error(f"GET request failed: {e}")
            if response := getattr(e, 'response', None):
                try:
                    error_detail = response.json()
                    raise ApiClientException(f"API error: {error_detail}")
                except ValueError:
                    pass
            raise ApiClientException(f"Request failed: {str(e)}")
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request to API
        
        :param endpoint: API endpoint (without base URL)
        :param data: Request data
        :return: Response data
        :raises ApiClientException: On request failure
        """
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        try:
            self._logger.info(f"Making POST request to {url}")
            response = requests.post(
                url,
                json=data,
                headers={**self.get_auth_headers(), "Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._logger.error(f"POST request failed: {e}")
            if response := getattr(e, 'response', None):
                try:
                    error_detail = response.json()
                    raise ApiClientException(f"API error: {error_detail}")
                except ValueError:
                    pass
            raise ApiClientException(f"Request failed: {str(e)}")
    
    def post_form(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request with form data to API
        
        :param endpoint: API endpoint (without base URL)
        :param data: Form data
        :return: Response data
        :raises ApiClientException: On request failure
        """
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        try:
            self._logger.info(f"Making form POST request to {url}")
            # FastAPI's OAuth2PasswordRequestForm expects form data
            # Para FastAPI, el Content-Type debe ser correcto para OAuth2 form
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(
                url,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._logger.error(f"POST form request failed: {e}")
            if "Connection refused" in str(e) or "Failed to establish a new connection" in str(e):
                raise ApiClientException(f"API server not available: {str(e)}")
                
            if response := getattr(e, 'response', None):
                try:
                    error_detail = response.json()
                    raise ApiClientException(f"API error: {error_detail}")
                except ValueError:
                    pass
            raise ApiClientException(f"Request failed: {str(e)}")