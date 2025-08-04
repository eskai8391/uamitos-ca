from typing import List, Dict, Any, Optional
import logging
from PySide6.QtCore import QObject, Signal

from infrastructure.api_client import UserApiClient


class UserViewModel(QObject):
    """ViewModel for handling user-related operations"""
    
    # Signals
    usersLoaded = Signal(list)
    userAdded = Signal(dict)
    userUpdated = Signal(dict)
    userDeleted = Signal(str)
    error = Signal(str)
    
    def __init__(self, api_client: UserApiClient):
        """
        Initialize user view model
        
        :param api_client: User API client
        """
        super().__init__()
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
        self._users = []
        
        # Log API client state for debugging
        self._logger.info(f"UserViewModel initialized with UserApiClient instance: {id(api_client)}")
        if hasattr(api_client, "_api_client") and hasattr(api_client._api_client, "_token"):
            token = api_client._api_client._token
            self._logger.info(f"API token present: {bool(token)}")
        self._role_filter = None
        self._search_filter = None
        
    def load_users(self) -> None:
        """Load users from API"""
        try:
            # Get users with filters
            self._logger.info(f"Loading users with filters: role={self._role_filter}, search={self._search_filter}")
            self._users = self._api_client.get_users(self._role_filter, self._search_filter)
                
            # Emit signal with loaded users
            self.usersLoaded.emit(self._users)
        except Exception as e:
            error_msg = f"Failed to load users: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            # Return empty list on error
            self._users = []
            self.usersLoaded.emit([])
            
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Get loaded users
        
        :return: List of user data
        """
        return self._users
        
    def add_user(self, user_data: Dict[str, Any]) -> None:
        """
        Add a new user
        
        :param user_data: User data to add
        """
        try:
            result = self._api_client.add_user(user_data)
            self._logger.info(f"Added new user: {user_data.get('name')}")
            self.userAdded.emit(result)
            # Reload users to update the list
            self.load_users()
        except Exception as e:
            error_msg = f"Failed to add user: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> None:
        """
        Update an existing user
        
        :param user_id: ID of user to update
        :param user_data: New user data
        """
        try:
            result = self._api_client.update_user(user_id, user_data)
            self._logger.info(f"Updated user {user_id}")
            self.userUpdated.emit(result)
            # Reload users to update the list
            self.load_users()
        except Exception as e:
            error_msg = f"Failed to update user: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def delete_user(self, user_id: str) -> None:
        """
        Delete a user
        
        :param user_id: ID of user to delete
        """
        try:
            self._api_client.delete_user(user_id)
            self._logger.info(f"Deleted user {user_id}")
            self.userDeleted.emit(user_id)
            # Reload users to update the list
            self.load_users()
        except Exception as e:
            error_msg = f"Failed to delete user: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Find user by ID
        
        :param user_id: User ID to find
        :return: User data or None if not found
        """
        for user in self._users:
            if user.get('id') == user_id or user.get('uuid') == user_id:
                return user
                
        try:
            # If not found in local cache, try to fetch from API
            return self._api_client.get_user_by_id(user_id)
        except Exception as e:
            self._logger.error(f"Failed to fetch user {user_id}: {e}")
            return None
            
    def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """
        Get users with a specific role
        
        :param role: Role to filter by
        :return: List of users with the specified role
        """
        return [u for u in self._users if u.get('role') == role]
        
    def set_role_filter(self, role: str) -> None:
        """
        Set role filter for users query
        
        :param role: Role to filter by, or None for all roles
        """
        if role == "Todos":
            self._role_filter = None
        else:
            self._role_filter = role
            
    def set_search_filter(self, search_text: str) -> None:
        """
        Set search filter for users query
        
        :param search_text: Text to search for in user names or emails
        """
        if not search_text:
            self._search_filter = None
        else:
            self._search_filter = search_text