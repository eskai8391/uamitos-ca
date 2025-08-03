import logging
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer

from infrastructure.api_client import TeacherApiClient


class TeacherViewModel(QObject):
    """
    View model for teacher-related data
    Handles fetching and processing teacher data from API
    """
    
    # Signals
    teachersLoaded = Signal(list)  # List of teacher data
    teacherDetailsLoaded = Signal(dict)  # Teacher details
    teacherSubjectsLoaded = Signal(list)  # List of subjects taught by a teacher
    error = Signal(str)  # Error message
    
    def __init__(self, teacher_api_client: TeacherApiClient, parent: Optional[QObject] = None):
        """
        Initialize the teacher view model
        
        :param teacher_api_client: TeacherApiClient instance
        :param parent: Parent QObject
        """
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._api_client = teacher_api_client
        # Log API client state to debug token issues
        self._logger.info(f"TeacherViewModel initialized with TeacherApiClient instance: {id(teacher_api_client)}")
        if hasattr(teacher_api_client, "_api_client") and hasattr(teacher_api_client._api_client, "_token"):
            token = teacher_api_client._api_client._token
            self._logger.info(f"API token present: {bool(token)}")
        
        # Properties
        self._teachers = []
        self._current_teacher = None
        self._teacher_subjects = []
        self._is_loading = False
        
        # Setup auto-refresh timer (refresh every 5 minutes)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.load_teachers)
        self._refresh_timer.start(300000)  # 5 minutes
    
    @Property(bool)
    def is_loading(self) -> bool:
        return self._is_loading
    
    @is_loading.setter
    def is_loading(self, value: bool) -> None:
        if self._is_loading != value:
            self._is_loading = value
    
    @Property(list)
    def teachers(self) -> List[Dict[str, Any]]:
        return self._teachers
    
    @Property(dict)
    def current_teacher(self) -> Optional[Dict[str, Any]]:
        return self._current_teacher
    
    @Property(list)
    def teacher_subjects(self) -> List[Dict[str, Any]]:
        return self._teacher_subjects
    
    @Slot()
    def load_teachers(self) -> None:
        """Load all teachers"""
        self._logger.info("Loading teachers")
        self.is_loading = True
        
        try:
            teachers = self._api_client.get_all_teachers()
            self._teachers = teachers
            self.teachersLoaded.emit(teachers)
            self._logger.info(f"Loaded {len(teachers)} teachers")
        except Exception as e:
            self._logger.error(f"Error loading teachers: {e}")
            self.error.emit(f"Error loading teachers: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_teacher_details(self, teacher_uuid: str) -> None:
        """
        Load details for a specific teacher
        
        :param teacher_uuid: Teacher UUID
        """
        self._logger.info(f"Loading teacher details for {teacher_uuid}")
        self.is_loading = True
        
        try:
            teacher = self._api_client.get_teacher_by_id(teacher_uuid)
            if teacher:
                self._current_teacher = teacher
                self.teacherDetailsLoaded.emit(teacher)
                self._logger.info(f"Loaded details for teacher {teacher_uuid}")
                
                # Also load subjects
                self.load_teacher_subjects(teacher_uuid)
            else:
                self._logger.warning(f"Teacher {teacher_uuid} not found")
                self.error.emit(f"Teacher not found")
        except Exception as e:
            self._logger.error(f"Error loading teacher details: {e}")
            self.error.emit(f"Error loading teacher details: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_teacher_subjects(self, teacher_uuid: str) -> None:
        """
        Load subjects taught by a specific teacher
        
        :param teacher_uuid: Teacher UUID
        """
        self._logger.info(f"Loading subjects for teacher {teacher_uuid}")
        
        try:
            subjects = self._api_client.get_teacher_subjects(teacher_uuid)
            self._teacher_subjects = subjects
            self.teacherSubjectsLoaded.emit(subjects)
            self._logger.info(f"Loaded {len(subjects)} subjects for teacher {teacher_uuid}")
        except Exception as e:
            self._logger.error(f"Error loading teacher subjects: {e}")
            self.error.emit(f"Error loading subjects: {str(e)}")
    
    def format_teachers_for_display(self) -> List[tuple]:
        """
        Format teacher data for display in a list
        
        :return: List of tuples with (name, subject)
        """
        result = []
        for teacher in self._teachers:
            name = f"{teacher.get('first_name', '')} {teacher.get('last_name', '')}"
            specialization = teacher.get('specialization', 'General')
            result.append((name, specialization))
        
        return result
    
    def find_teacher_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a teacher by their name
        
        :param name: Teacher name (first + last)
        :return: Teacher data or None if not found
        """
        for teacher in self._teachers:
            full_name = f"{teacher.get('first_name', '')} {teacher.get('last_name', '')}"
            if full_name.lower() == name.lower():
                return teacher
        return None
    
    def get_teacher_uuid_by_name(self, name: str) -> Optional[str]:
        """
        Get a teacher's UUID by their name
        
        :param name: Teacher name (first + last)
        :return: Teacher UUID or None if not found
        """
        teacher = self.find_teacher_by_name(name)
        if teacher:
            return teacher.get('uuid')
        return None
    
    def dispose(self) -> None:
        """Clean up resources"""
        self._refresh_timer.stop()