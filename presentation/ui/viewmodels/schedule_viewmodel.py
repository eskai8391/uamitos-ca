from typing import List, Dict, Any, Optional
import logging
from PySide6.QtCore import QObject, Signal

from infrastructure.api_client import ScheduleApiClient


class ScheduleViewModel(QObject):
    """ViewModel for handling schedule-related operations"""
    
    # Signals
    scheduleLoaded = Signal(dict)
    classAdded = Signal(dict)
    classUpdated = Signal(dict)
    classRemoved = Signal(str)
    error = Signal(str)
    
    def __init__(self, api_client: ScheduleApiClient, user_id: Optional[str] = None, role: Optional[str] = None):
        """
        Initialize schedule view model
        
        :param api_client: Schedule API client
        :param user_id: Optional user ID to filter schedule
        :param role: User role (student, teacher, admin)
        """
        super().__init__()
        self._api_client = api_client
        self._user_id = user_id
        self._role = role
        self._logger = logging.getLogger(__name__)
        self._schedule = {}
        
    def load_schedule(self) -> None:
        """Load schedule from API"""
        try:
            if self._user_id and self._role:
                # Get schedule for specific user and role
                self._logger.info(f"Loading schedule for {self._role} {self._user_id}")
                
                if self._role == "student":
                    self._schedule = self._api_client.get_student_schedule(self._user_id)
                elif self._role == "teacher":
                    self._schedule = self._api_client.get_teacher_schedule(self._user_id)
                else:
                    self._schedule = self._api_client.get_schedule(self._user_id)
            else:
                # Get general schedule
                self._logger.info("Loading general schedule")
                self._schedule = self._api_client.get_general_schedule()
                
            # Emit signal with loaded schedule
            self.scheduleLoaded.emit(self._schedule)
        except Exception as e:
            error_msg = f"Failed to load schedule: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            # Return empty dictionary on error
            self._schedule = {}
            self.scheduleLoaded.emit({})
            
    def get_schedule(self) -> Dict[str, Any]:
        """
        Get loaded schedule
        
        :return: Schedule data
        """
        return self._schedule
        
    def add_class(self, class_data: Dict[str, Any]) -> None:
        """
        Add a new class to the schedule
        
        :param class_data: Class data to add
        """
        try:
            result = self._api_client.add_class(class_data)
            self._logger.info(f"Added new class: {class_data.get('subject', 'Unknown')}")
            self.classAdded.emit(result)
            # Reload schedule to update
            self.load_schedule()
        except Exception as e:
            error_msg = f"Failed to add class: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def update_class(self, class_id: str, class_data: Dict[str, Any]) -> None:
        """
        Update an existing class
        
        :param class_id: ID of class to update
        :param class_data: New class data
        """
        try:
            result = self._api_client.update_class(class_id, class_data)
            self._logger.info(f"Updated class {class_id}")
            self.classUpdated.emit(result)
            # Reload schedule to update
            self.load_schedule()
        except Exception as e:
            error_msg = f"Failed to update class: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def remove_class(self, class_id: str) -> None:
        """
        Remove a class from the schedule
        
        :param class_id: ID of class to remove
        """
        try:
            self._api_client.remove_class(class_id)
            self._logger.info(f"Removed class {class_id}")
            self.classRemoved.emit(class_id)
            # Reload schedule to update
            self.load_schedule()
        except Exception as e:
            error_msg = f"Failed to remove class: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def get_classes_by_day(self, day: str) -> List[Dict[str, Any]]:
        """
        Get classes for a specific day
        
        :param day: Day of week (e.g., "monday", "tuesday")
        :return: List of classes for that day
        """
        day_classes = self._schedule.get(day.lower(), [])
        return day_classes
        
    def set_user_id(self, user_id: str, role: str) -> None:
        """
        Set user ID and role to filter schedule
        
        :param user_id: User ID
        :param role: User role
        """
        self._user_id = user_id
        self._role = role