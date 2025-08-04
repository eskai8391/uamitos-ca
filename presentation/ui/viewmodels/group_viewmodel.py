import logging
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer

from infrastructure.api_client import GroupApiClient


class GroupViewModel(QObject):
    """
    View model for group-related data
    Handles fetching and processing group data from API
    """
    
    # Signals
    groupsLoaded = Signal(list)  # List of group data
    groupDetailsLoaded = Signal(dict)  # Group details
    teacherGroupsLoaded = Signal(list)  # Groups taught by a teacher
    studentGroupsLoaded = Signal(list)  # Groups a student is enrolled in
    groupStudentsLoaded = Signal(list)  # Students in a group
    error = Signal(str)  # Error message
    
    def __init__(self, group_api_client: GroupApiClient, parent: Optional[QObject] = None):
        """
        Initialize the group view model
        
        :param group_api_client: GroupApiClient instance
        :param parent: Parent QObject
        """
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._api_client = group_api_client
        
        # Properties
        self._groups = []
        self._current_group = None
        self._is_loading = False
        
        # Setup auto-refresh timer (refresh every 5 minutes)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.load_groups)
        self._refresh_timer.start(300000)  # 5 minutes
    
    @Property(bool)
    def is_loading(self) -> bool:
        return self._is_loading
    
    @is_loading.setter
    def is_loading(self, value: bool) -> None:
        if self._is_loading != value:
            self._is_loading = value
    
    @Property(list)
    def groups(self) -> List[Dict[str, Any]]:
        return self._groups
    
    @Property(dict)
    def current_group(self) -> Optional[Dict[str, Any]]:
        return self._current_group
    
    @Slot()
    def load_groups(self) -> None:
        """Load all groups"""
        self._logger.info("Loading groups")
        self.is_loading = True
        
        try:
            groups = self._api_client.get_all_groups()
            self._groups = groups
            self.groupsLoaded.emit(groups)
            self._logger.info(f"Loaded {len(groups)} groups")
        except Exception as e:
            self._logger.error(f"Error loading groups: {e}")
            self.error.emit(f"Error loading groups: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_group_details(self, group_uuid: str) -> None:
        """
        Load details for a specific group
        
        :param group_uuid: Group UUID
        """
        self._logger.info(f"Loading group details for {group_uuid}")
        self.is_loading = True
        
        try:
            group = self._api_client.get_group_by_id(group_uuid)
            if group:
                self._current_group = group
                self.groupDetailsLoaded.emit(group)
                self._logger.info(f"Loaded details for group {group_uuid}")
            else:
                self._logger.warning(f"Group {group_uuid} not found")
                self.error.emit(f"Group not found")
        except Exception as e:
            self._logger.error(f"Error loading group details: {e}")
            self.error.emit(f"Error loading group details: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_teacher_groups(self, teacher_uuid: str) -> None:
        """
        Load groups taught by a specific teacher
        
        :param teacher_uuid: Teacher UUID
        """
        self._logger.info(f"Loading groups for teacher {teacher_uuid}")
        self.is_loading = True
        
        try:
            groups = self._api_client.get_groups_by_teacher(teacher_uuid)
            self.teacherGroupsLoaded.emit(groups)
            self._logger.info(f"Loaded {len(groups)} groups for teacher {teacher_uuid}")
        except Exception as e:
            self._logger.error(f"Error loading teacher's groups: {e}")
            self.error.emit(f"Error loading teacher's groups: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_student_groups(self, student_uuid: str) -> None:
        """
        Load groups that a student is enrolled in
        
        :param student_uuid: Student UUID
        """
        self._logger.info(f"Loading groups for student {student_uuid}")
        self.is_loading = True
        
        try:
            groups = self._api_client.get_groups_by_student(student_uuid)
            self.studentGroupsLoaded.emit(groups)
            self._logger.info(f"Loaded {len(groups)} groups for student {student_uuid}")
        except Exception as e:
            self._logger.error(f"Error loading student's groups: {e}")
            self.error.emit(f"Error loading student's groups: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str, str)
    def add_student_to_group(self, group_uuid: str, student_uuid: str) -> bool:
        """
        Add a student to a group
        
        :param group_uuid: Group UUID
        :param student_uuid: Student UUID
        :return: True if successful, False otherwise
        """
        self._logger.info(f"Adding student {student_uuid} to group {group_uuid}")
        self.is_loading = True
        
        try:
            success = self._api_client.add_student_to_group(group_uuid, student_uuid)
            if success:
                self._logger.info(f"Added student {student_uuid} to group {group_uuid}")
                # Reload group details to reflect the change
                self.load_group_details(group_uuid)
                return True
            else:
                self._logger.warning(f"Failed to add student {student_uuid} to group {group_uuid}")
                self.error.emit("Failed to add student to group")
                return False
        except Exception as e:
            self._logger.error(f"Error adding student to group: {e}")
            self.error.emit(f"Error adding student to group: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    @Slot(str, str)
    def remove_student_from_group(self, group_uuid: str, student_uuid: str) -> bool:
        """
        Remove a student from a group
        
        :param group_uuid: Group UUID
        :param student_uuid: Student UUID
        :return: True if successful, False otherwise
        """
        self._logger.info(f"Removing student {student_uuid} from group {group_uuid}")
        self.is_loading = True
        
        try:
            success = self._api_client.remove_student_from_group(group_uuid, student_uuid)
            if success:
                self._logger.info(f"Removed student {student_uuid} from group {group_uuid}")
                # Reload group details to reflect the change
                self.load_group_details(group_uuid)
                return True
            else:
                self._logger.warning(f"Failed to remove student {student_uuid} from group {group_uuid}")
                self.error.emit("Failed to remove student from group")
                return False
        except Exception as e:
            self._logger.error(f"Error removing student from group: {e}")
            self.error.emit(f"Error removing student from group: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    @Slot(dict)
    def create_group(self, group_data: Dict[str, Any]) -> bool:
        """
        Create a new group
        
        :param group_data: Group data
        :return: True if successful, False otherwise
        """
        self._logger.info(f"Creating new group")
        self.is_loading = True
        
        try:
            result = self._api_client.create_group(group_data)
            if result:
                self._logger.info(f"Created new group with UUID {result.get('uuid')}")
                # Reload groups to reflect the change
                self.load_groups()
                return True
            else:
                self._logger.warning(f"Failed to create group")
                self.error.emit("Failed to create group")
                return False
        except Exception as e:
            self._logger.error(f"Error creating group: {e}")
            self.error.emit(f"Error creating group: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    @Slot(str)
    def delete_group(self, group_uuid: str) -> bool:
        """
        Delete a group
        
        :param group_uuid: Group UUID
        :return: True if successful, False otherwise
        """
        self._logger.info(f"Deleting group {group_uuid}")
        self.is_loading = True
        
        try:
            success = self._api_client.delete_group(group_uuid)
            if success:
                self._logger.info(f"Deleted group {group_uuid}")
                # Reload groups to reflect the change
                self.load_groups()
                return True
            else:
                self._logger.warning(f"Failed to delete group {group_uuid}")
                self.error.emit("Failed to delete group")
                return False
        except Exception as e:
            self._logger.error(f"Error deleting group: {e}")
            self.error.emit(f"Error deleting group: {str(e)}")
            return False
        finally:
            self.is_loading = False
    
    def get_day_name(self, day_of_week: int) -> str:
        """
        Get the name of the day from its index
        
        :param day_of_week: Day index (0=Monday, 1=Tuesday, etc.)
        :return: Day name
        """
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        if 0 <= day_of_week < len(days):
            return days[day_of_week]
        return "Desconocido"
    
    def dispose(self) -> None:
        """Clean up resources"""
        self._refresh_timer.stop()