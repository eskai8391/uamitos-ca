import logging
from typing import List, Dict, Any, Optional

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class StudentApiClient:
    """API client for student-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize student API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        """
        Get all students
        
        :return: List of student data
        """
        try:
            # Call the API endpoint to get students
            students_data = self._api_client.get("students")
            if isinstance(students_data, list):
                return students_data
            else:
                self._logger.warning("Unexpected students data format")
                return []
        except Exception as e:
            self._logger.error(f"Failed to fetch students: {e}")
            # Provide some mock data in case of error
            return self._get_mock_students()
    
    def get_student_by_id(self, student_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get student by UUID
        
        :param student_uuid: Student UUID
        :return: Student data or None if not found
        """
        try:
            # In a complete implementation, this would call the API endpoint
            # For now, we'll use our mock data since student/{id} route isn't implemented
            students = self._get_mock_students()
            for student in students:
                if student.get("uuid") == student_uuid:
                    return student
            
            return None
            
        except Exception as e:
            self._logger.error(f"Failed to fetch student: {e}")
            return None
    
    def get_student_grades(self, student_uuid: str) -> List[Dict[str, Any]]:
        """
        Get grades for a student
        
        :param student_uuid: Student UUID
        :return: List of grades data
        """
        # In a real implementation, this would call the API
        # For demonstration, return mock data
        return [
            {"subject": "Matemáticas", "period1": 85, "period2": 90, "period3": 88, "final": 88},
            {"subject": "Historia", "period1": 78, "period2": 82, "period3": 85, "final": 82},
            {"subject": "Física", "period1": 92, "period2": 88, "period3": 95, "final": 92},
            {"subject": "Literatura", "period1": 88, "period2": 90, "period3": 87, "final": 88},
            {"subject": "Inglés", "period1": 95, "period2": 92, "period3": 97, "final": 95}
        ]
    
    def get_student_attendance(self, student_uuid: str) -> List[Dict[str, Any]]:
        """
        Get attendance records for a student
        
        :param student_uuid: Student UUID
        :return: List of attendance records
        """
        # In a real implementation, this would call the API
        # For demonstration, return mock data
        return [
            {"date": "2025-07-01", "status": "Presente", "comment": "-"},
            {"date": "2025-06-30", "status": "Presente", "comment": "-"},
            {"date": "2025-06-29", "status": "Ausente", "comment": "Justificada por enfermedad"},
            {"date": "2025-06-28", "status": "Presente", "comment": "-"},
            {"date": "2025-06-27", "status": "Presente", "comment": "-"}
        ]
    
    def _get_mock_students(self) -> List[Dict[str, Any]]:
        """
        Generate mock student data for fallback
        
        :return: List of mock student data
        """
        return [
            {
                "uuid": "stu-001",
                "email": "ana.lopez@uamitos.edu.mx",
                "first_name": "Ana",
                "last_name": "López",
                "role": "student",
                "is_active": True,
                "last_login": "2025-07-01T08:30:00",
                "age": 16,
                "phone": "+52-555-123-4567",
                "address": "Calle Principal 123",
                "city": "México",
                "state": "CDMX",
                "zip_code": "12345",
                "grade_level": "3°A",
                "attendance_rate": 95
            },
            {
                "uuid": "stu-002",
                "email": "luis.perez@uamitos.edu.mx",
                "first_name": "Luis",
                "last_name": "Pérez",
                "role": "student",
                "is_active": True,
                "last_login": "2025-07-01T09:15:00",
                "age": 15,
                "phone": "+52-555-234-5678",
                "address": "Av. Reforma 456",
                "city": "México",
                "state": "CDMX",
                "zip_code": "12345",
                "grade_level": "2°B",
                "attendance_rate": 89
            },
            {
                "uuid": "stu-003",
                "email": "marta.sanchez@uamitos.edu.mx",
                "first_name": "Marta",
                "last_name": "Sánchez",
                "role": "student",
                "is_active": True,
                "last_login": "2025-07-01T10:00:00",
                "age": 14,
                "phone": "+52-555-345-6789",
                "address": "Calle Juárez 789",
                "city": "México",
                "state": "CDMX",
                "zip_code": "12345",
                "grade_level": "1°C",
                "attendance_rate": 92
            },
            {
                "uuid": "stu-004",
                "email": "carlos.gomez@uamitos.edu.mx",
                "first_name": "Carlos",
                "last_name": "Gómez",
                "role": "student",
                "is_active": True,
                "last_login": "2025-07-01T11:30:00",
                "age": 16,
                "phone": "+52-555-456-7890",
                "address": "Av. Insurgentes 101",
                "city": "México",
                "state": "CDMX",
                "zip_code": "12345",
                "grade_level": "3°B",
                "attendance_rate": 85
            },
            {
                "uuid": "stu-005",
                "email": "lucia.torres@uamitos.edu.mx",
                "first_name": "Lucía",
                "last_name": "Torres",
                "role": "student",
                "is_active": True,
                "last_login": "2025-07-01T12:45:00",
                "age": 15,
                "phone": "+52-555-567-8901",
                "address": "Calle 5 de Mayo 202",
                "city": "México",
                "state": "CDMX",
                "zip_code": "12345",
                "grade_level": "2°C",
                "attendance_rate": 95
            }
        ]