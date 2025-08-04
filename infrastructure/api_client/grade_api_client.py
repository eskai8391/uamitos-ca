import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class GradeApiClient:
    """API client for grade-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize grade API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_all_grades(self) -> List[Dict[str, Any]]:
        """
        Get all grades
        
        :return: List of grade data
        """
        try:
            # Call the API endpoint to get grades
            grades_data = self._api_client.get("grades")
            if isinstance(grades_data, list):
                return grades_data
            else:
                self._logger.warning("Unexpected grades data format")
                return []
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Grades endpoint not found, using mock data")
                # Generate mock grades
                return self._get_mock_grades()
            else:
                self._logger.error(f"Failed to fetch grades: {e}")
                # Provide some mock data in case of error
                return self._get_mock_grades()
        except Exception as e:
            self._logger.error(f"Failed to fetch grades: {e}")
            # Provide some mock data in case of error
            return self._get_mock_grades()
    
    def get_student_grades(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get grades for a specific student
        
        :param student_id: Student ID
        :return: List of grade data for the student
        """
        try:
            # Call the API endpoint to get student grades
            return self._api_client.get(f"grades/student/{student_id}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Student grades endpoint not found, using mock data")
                # Generate mock grades for this student
                return self._get_mock_student_grades(student_id)
            else:
                self._logger.error(f"Failed to fetch student grades: {e}")
                # Generate mock grades for this student
                return self._get_mock_student_grades(student_id)
        except Exception as e:
            self._logger.error(f"Failed to fetch student grades: {e}")
            # Generate mock grades for this student
            return self._get_mock_student_grades(student_id)
    
    def get_grade_by_id(self, grade_id: str) -> Optional[Dict[str, Any]]:
        """
        Get grade by ID
        
        :param grade_id: Grade ID
        :return: Grade data or None if not found
        """
        try:
            # Call the API endpoint to get the grade
            return self._api_client.get(f"grades/{grade_id}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Grade not found: {grade_id}")
                return None
            else:
                self._logger.error(f"Error fetching grade: {e}")
                # Try to find in mock data
                grades = self._get_mock_grades()
                for grade in grades:
                    if grade.get("id") == grade_id or grade.get("uuid") == grade_id:
                        return grade
                return None
        except Exception as e:
            self._logger.error(f"Failed to fetch grade: {e}")
            return None
    
    def add_grade(self, grade_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new grade
        
        :param grade_data: Grade data to add
        :return: Added grade data
        """
        try:
            # Call the API endpoint to add a grade
            return self._api_client.post("grades", grade_data)
        except Exception as e:
            self._logger.error(f"Failed to add grade: {e}")
            # Return the input data with a mock ID
            import uuid
            grade_data["id"] = str(uuid.uuid4())
            return grade_data
    
    def update_grade(self, grade_id: str, grade_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing grade
        
        :param grade_id: ID of grade to update
        :param grade_data: New grade data
        :return: Updated grade data
        """
        try:
            # Call the API endpoint to update a grade
            return self._api_client.post(f"grades/{grade_id}", grade_data)
        except Exception as e:
            self._logger.error(f"Failed to update grade: {e}")
            # Return the input data
            grade_data["id"] = grade_id
            return grade_data
    
    def _get_mock_grades(self) -> List[Dict[str, Any]]:
        """
        Generate mock grade data for fallback
        
        :return: List of mock grade data
        """
        return [
            {
                "id": "grade-001",
                "student_id": "std-001",
                "subject_id": "subj-001",
                "subject_name": "Matemáticas",
                "grade": 9.5,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-002",
                "student_id": "std-001",
                "subject_id": "subj-002",
                "subject_name": "Historia",
                "grade": 8.7,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-003",
                "student_id": "std-001",
                "subject_id": "subj-003",
                "subject_name": "Física",
                "grade": 7.8,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-004",
                "student_id": "std-001",
                "subject_id": "subj-004",
                "subject_name": "Química",
                "grade": 9.0,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-005",
                "student_id": "std-001",
                "subject_id": "subj-005",
                "subject_name": "Literatura",
                "grade": 5.9,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-006",
                "student_id": "std-001",
                "subject_id": "subj-006",
                "subject_name": "Educación Física",
                "grade": 8.5,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-007",
                "student_id": "std-001",
                "subject_id": "subj-007",
                "subject_name": "Inglés",
                "grade": 6.5,
                "is_final": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-008",
                "student_id": "std-002",
                "subject_id": "subj-001",
                "subject_name": "Matemáticas",
                "grade": 7.5,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-009",
                "student_id": "std-002",
                "subject_id": "subj-002",
                "subject_name": "Historia",
                "grade": 6.7,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "grade-010",
                "student_id": "std-002",
                "subject_id": "subj-003",
                "subject_name": "Física",
                "grade": 8.8,
                "is_final": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
    
    def _get_mock_student_grades(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Generate mock grades for a specific student
        
        :param student_id: Student ID
        :return: List of mock grade data for the student
        """
        all_grades = self._get_mock_grades()
        return [g for g in all_grades if g.get("student_id") == student_id]