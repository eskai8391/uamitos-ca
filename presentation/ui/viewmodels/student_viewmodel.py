import logging
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer

from infrastructure.api_client import StudentApiClient


class StudentViewModel(QObject):
    """
    View model for student-related data
    Handles fetching and processing student data from API
    """
    
    # Signals
    studentsLoaded = Signal(list)  # List of student data
    studentDetailsLoaded = Signal(dict)  # Student details
    gradesLoaded = Signal(list)  # List of grades
    attendanceLoaded = Signal(list)  # List of attendance records
    error = Signal(str)  # Error message
    
    def __init__(self, student_api_client: StudentApiClient, parent: Optional[QObject] = None):
        """
        Initialize the student view model
        
        :param student_api_client: StudentApiClient instance
        :param parent: Parent QObject
        """
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._api_client = student_api_client
        # Log API client state to debug token issues
        self._logger.info(f"StudentViewModel initialized with StudentApiClient instance: {id(student_api_client)}")
        if hasattr(student_api_client, "_api_client") and hasattr(student_api_client._api_client, "_token"):
            token = student_api_client._api_client._token
            self._logger.info(f"API token present: {bool(token)}")
        
        # Properties
        self._students = []
        self._current_student = None
        self._grades = []
        self._attendance = []
        self._is_loading = False
        
        # Setup auto-refresh timer (refresh every 5 minutes)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.load_students)
        self._refresh_timer.start(300000)  # 5 minutes
    
    @Property(bool)
    def is_loading(self) -> bool:
        return self._is_loading
    
    @is_loading.setter
    def is_loading(self, value: bool) -> None:
        if self._is_loading != value:
            self._is_loading = value
    
    @Property(list)
    def students(self) -> List[Dict[str, Any]]:
        return self._students
    
    @Property(dict)
    def current_student(self) -> Optional[Dict[str, Any]]:
        return self._current_student
    
    @Property(list)
    def grades(self) -> List[Dict[str, Any]]:
        return self._grades
    
    @Property(list)
    def attendance(self) -> List[Dict[str, Any]]:
        return self._attendance
    
    @Slot()
    def load_students(self) -> None:
        """Load all students"""
        self._logger.info("Loading students")
        self.is_loading = True
        
        try:
            students = self._api_client.get_all_students()
            self._students = students
            self.studentsLoaded.emit(students)
            self._logger.info(f"Loaded {len(students)} students")
        except Exception as e:
            self._logger.error(f"Error loading students: {e}")
            self.error.emit(f"Error loading students: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_student_details(self, student_uuid: str) -> None:
        """
        Load details for a specific student
        
        :param student_uuid: Student UUID
        """
        self._logger.info(f"Loading student details for {student_uuid}")
        self.is_loading = True
        
        try:
            student = self._api_client.get_student_by_id(student_uuid)
            if student:
                self._current_student = student
                self.studentDetailsLoaded.emit(student)
                self._logger.info(f"Loaded details for student {student_uuid}")
                
                # Also load grades and attendance
                self.load_student_grades(student_uuid)
                self.load_student_attendance(student_uuid)
            else:
                self._logger.warning(f"Student {student_uuid} not found")
                self.error.emit(f"Student not found")
        except Exception as e:
            self._logger.error(f"Error loading student details: {e}")
            self.error.emit(f"Error loading student details: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_student_grades(self, student_uuid: str) -> None:
        """
        Load grades for a specific student
        
        :param student_uuid: Student UUID
        """
        self._logger.info(f"Loading grades for student {student_uuid}")
        
        try:
            grades = self._api_client.get_student_grades(student_uuid)
            self._grades = grades
            self.gradesLoaded.emit(grades)
            self._logger.info(f"Loaded {len(grades)} grades for student {student_uuid}")
        except Exception as e:
            self._logger.error(f"Error loading student grades: {e}")
            self.error.emit(f"Error loading grades: {str(e)}")
    
    @Slot(str)
    def load_student_attendance(self, student_uuid: str) -> None:
        """
        Load attendance records for a specific student
        
        :param student_uuid: Student UUID
        """
        self._logger.info(f"Loading attendance for student {student_uuid}")
        
        try:
            attendance = self._api_client.get_student_attendance(student_uuid)
            self._attendance = attendance
            self.attendanceLoaded.emit(attendance)
            self._logger.info(f"Loaded {len(attendance)} attendance records for student {student_uuid}")
        except Exception as e:
            self._logger.error(f"Error loading student attendance: {e}")
            self.error.emit(f"Error loading attendance: {str(e)}")
    
    def format_students_for_table(self) -> List[tuple]:
        """
        Format student data for display in a table
        
        :return: List of tuples with (name, grade, attendance)
        """
        result = []
        for student in self._students:
            name = f"{student.get('first_name', '')} {student.get('last_name', '')}"
            grade_level = student.get('grade_level', 'N/A')
            attendance = f"{student.get('attendance_rate', 0)}%"
            result.append((name, grade_level, attendance))
        
        return result
    
    def dispose(self) -> None:
        """Clean up resources"""
        self._refresh_timer.stop()