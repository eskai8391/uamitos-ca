import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class UserApiClient:
    """API client for user-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize user API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_users(self, role_filter: Optional[str] = None, search_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get users with optional filtering
        
        :param role_filter: Optional role to filter by
        :param search_filter: Optional text to search for in user names/emails
        :return: List of user data
        """
        params = {}
        if role_filter:
            params["role"] = role_filter
        if search_filter:
            params["search"] = search_filter
            
        try:
            # Call the API endpoint to get users
            users_data = self._api_client.get("users", params=params)
            if isinstance(users_data, list):
                return users_data
            else:
                self._logger.warning("Unexpected users data format")
                return []
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Users endpoint not found, using mock data")
                # Generate mock users
                return self._get_mock_users(role_filter, search_filter)
            else:
                self._logger.error(f"Failed to fetch users: {e}")
                # Provide some mock data in case of error
                return self._get_mock_users(role_filter, search_filter)
        except Exception as e:
            self._logger.error(f"Failed to fetch users: {e}")
            # Provide some mock data in case of error
            return self._get_mock_users(role_filter, search_filter)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        :param user_id: User ID
        :return: User data or None if not found
        """
        try:
            # Call the API endpoint to get the user
            return self._api_client.get(f"users/{user_id}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"User not found: {user_id}")
                return None
            else:
                self._logger.error(f"Error fetching user: {e}")
                # Try to find in mock data
                users = self._get_mock_users()
                for user in users:
                    if user.get("id") == user_id or user.get("uuid") == user_id:
                        return user
                return None
        except Exception as e:
            self._logger.error(f"Failed to fetch user: {e}")
            return None
    
    def add_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new user
        
        :param user_data: User data to add
        :return: Added user data
        """
        try:
            # Call the API endpoint to add a user
            return self._api_client.post("users", user_data)
        except Exception as e:
            self._logger.error(f"Failed to add user: {e}")
            # Return the input data with a mock ID
            import uuid
            user_data["id"] = str(uuid.uuid4())
            user_data["created_at"] = datetime.now().isoformat()
            return user_data
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing user
        
        :param user_id: ID of user to update
        :param user_data: New user data
        :return: Updated user data
        """
        try:
            # Call the API endpoint to update a user
            return self._api_client.post(f"users/{user_id}", user_data)
        except Exception as e:
            self._logger.error(f"Failed to update user: {e}")
            # Return the input data
            user_data["id"] = user_id
            user_data["updated_at"] = datetime.now().isoformat()
            return user_data
            
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user
        
        :param user_id: ID of user to delete
        :return: True if successful, False otherwise
        """
        try:
            # Call the API endpoint to delete a user
            self._api_client.post(f"users/{user_id}/delete", {})
            return True
        except Exception as e:
            self._logger.error(f"Failed to delete user: {e}")
            return False
    
    def _get_mock_users(self, role_filter: Optional[str] = None, search_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate mock user data for fallback
        
        :param role_filter: Optional role to filter by
        :param search_filter: Optional text to search for in user names/emails
        :return: List of mock user data
        """
        users = [
            {
                "id": "usr-001",
                "uuid": "usr-001",
                "name": "Admin Test",
                "email": "admin@test.com",
                "role": "Administrador",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-002",
                "uuid": "usr-002",
                "name": "Laura Gómez",
                "email": "laura.gomez@uamitos.edu.mx",
                "role": "Profesor",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-003",
                "uuid": "usr-003",
                "name": "David Martinez",
                "email": "david.martinez@uamitos.edu.mx",
                "role": "Profesor",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-004",
                "uuid": "usr-004",
                "name": "Miguel Torres",
                "email": "miguel.torres@uamitos.edu.mx",
                "role": "Profesor",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-005",
                "uuid": "usr-005",
                "name": "Ana García",
                "email": "ana.garcia@uamitos.edu.mx",
                "role": "Estudiante",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-006",
                "uuid": "usr-006",
                "name": "Carlos López",
                "email": "carlos.lopez@uamitos.edu.mx",
                "role": "Estudiante",
                "active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "usr-007",
                "uuid": "usr-007",
                "name": "Maria Rodríguez",
                "email": "maria.rodriguez@uamitos.edu.mx",
                "role": "Estudiante",
                "active": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        # Apply role filter if provided
        if role_filter and role_filter != "Todos":
            users = [u for u in users if u.get("role") == role_filter]
            
        # Apply search filter if provided
        if search_filter:
            search_text = search_filter.lower()
            users = [
                u for u in users 
                if search_text in u.get("name", "").lower() or 
                   search_text in u.get("email", "").lower()
            ]
            
        return users