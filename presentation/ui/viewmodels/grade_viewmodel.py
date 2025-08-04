from typing import List, Dict, Any, Optional
import logging
from PySide6.QtCore import QObject, Signal

from infrastructure.api_client import GradeApiClient


class GradeViewModel(QObject):
    """ViewModel for handling grade-related operations"""
    
    # Signals
    gradesLoaded = Signal(list)
    gradeAdded = Signal(dict)
    gradeUpdated = Signal(dict)
    error = Signal(str)
    
    def __init__(self, api_client: GradeApiClient, student_id: Optional[str] = None):
        """
        Initialize grade view model
        
        :param api_client: Grade API client
        :param student_id: Optional student ID to filter grades
        """
        super().__init__()
        self._api_client = api_client
        self._student_id = student_id
        self._logger = logging.getLogger(__name__)
        self._grades = []
        
    def load_grades(self) -> None:
        """Load grades from API"""
        try:
            if self._student_id:
                # Get grades for specific student
                self._logger.info(f"Loading grades for student {self._student_id}")
                self._grades = self._api_client.get_student_grades(self._student_id)
            else:
                # Get all grades
                self._logger.info("Loading all grades")
                self._grades = self._api_client.get_all_grades()
                
            # Emit signal with loaded grades
            self.gradesLoaded.emit(self._grades)
        except Exception as e:
            error_msg = f"Failed to load grades: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            # Return empty list on error
            self._grades = []
            self.gradesLoaded.emit([])
            
    def get_grades(self) -> List[Dict[str, Any]]:
        """
        Get loaded grades
        
        :return: List of grade data
        """
        return self._grades
        
    def add_grade(self, grade_data: Dict[str, Any]) -> None:
        """
        Add a new grade
        
        :param grade_data: Grade data to add
        """
        try:
            result = self._api_client.add_grade(grade_data)
            self._logger.info(f"Added new grade for student {grade_data.get('student_id')}")
            self.gradeAdded.emit(result)
            # Reload grades to update the list
            self.load_grades()
        except Exception as e:
            error_msg = f"Failed to add grade: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def update_grade(self, grade_id: str, grade_data: Dict[str, Any]) -> None:
        """
        Update an existing grade
        
        :param grade_id: ID of grade to update
        :param grade_data: New grade data
        """
        try:
            result = self._api_client.update_grade(grade_id, grade_data)
            self._logger.info(f"Updated grade {grade_id}")
            self.gradeUpdated.emit(result)
            # Reload grades to update the list
            self.load_grades()
        except Exception as e:
            error_msg = f"Failed to update grade: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def get_grade_by_id(self, grade_id: str) -> Optional[Dict[str, Any]]:
        """
        Find grade by ID
        
        :param grade_id: Grade ID to find
        :return: Grade data or None if not found
        """
        for grade in self._grades:
            if grade.get('id') == grade_id or grade.get('uuid') == grade_id:
                return grade
                
        return None
        
    def calculate_average(self) -> float:
        """
        Calculate average grade across all subjects
        
        :return: Average grade value
        """
        if not self._grades:
            return 0.0
            
        total = 0
        count = 0
        
        for grade in self._grades:
            grade_value = grade.get('grade')
            if grade_value is not None:
                try:
                    total += float(grade_value)
                    count += 1
                except (ValueError, TypeError):
                    # Skip non-numeric grades
                    pass
                    
        if count == 0:
            return 0.0
            
        return round(total / count, 2)
        
    def get_grades_by_subject(self, subject_id: str) -> List[Dict[str, Any]]:
        """
        Get grades for a specific subject
        
        :param subject_id: Subject ID
        :return: List of grade data for the subject
        """
        return [g for g in self._grades if g.get('subject_id') == subject_id]
        
    def set_student_id(self, student_id: str) -> None:
        """
        Set student ID to filter grades
        
        :param student_id: Student ID
        """
        self._student_id = student_id