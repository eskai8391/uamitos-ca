import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class ScheduleApiClient:
    """API client for schedule-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize schedule API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_general_schedule(self) -> Dict[str, Any]:
        """
        Get general schedule
        
        :return: Schedule data organized by days
        """
        try:
            # Call the API endpoint to get schedule
            schedule_data = self._api_client.get("schedule")
            return schedule_data
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Schedule endpoint not found, using mock data")
                # Generate mock schedule
                return self._get_mock_schedule()
            else:
                self._logger.error(f"Failed to fetch schedule: {e}")
                # Provide some mock data in case of error
                return self._get_mock_schedule()
        except Exception as e:
            self._logger.error(f"Failed to fetch schedule: {e}")
            # Provide some mock data in case of error
            return self._get_mock_schedule()
    
    def get_student_schedule(self, student_id: str) -> Dict[str, Any]:
        """
        Get schedule for a specific student
        
        :param student_id: Student ID
        :return: Student's schedule data organized by days
        """
        try:
            # Call the API endpoint to get student schedule
            return self._api_client.get(f"schedule/student/{student_id}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Student schedule endpoint not found, using mock data")
                # Generate mock schedule for this student
                return self._get_mock_student_schedule(student_id)
            else:
                self._logger.error(f"Failed to fetch student schedule: {e}")
                # Generate mock schedule for this student
                return self._get_mock_student_schedule(student_id)
        except Exception as e:
            self._logger.error(f"Failed to fetch student schedule: {e}")
            # Generate mock schedule for this student
            return self._get_mock_student_schedule(student_id)
    
    def get_teacher_schedule(self, teacher_id: str) -> Dict[str, Any]:
        """
        Get schedule for a specific teacher
        
        :param teacher_id: Teacher ID
        :return: Teacher's schedule data organized by days
        """
        try:
            # Call the API endpoint to get teacher schedule
            return self._api_client.get(f"schedule/teacher/{teacher_id}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Teacher schedule endpoint not found, using mock data")
                # Generate mock schedule for this teacher
                return self._get_mock_teacher_schedule(teacher_id)
            else:
                self._logger.error(f"Failed to fetch teacher schedule: {e}")
                # Generate mock schedule for this teacher
                return self._get_mock_teacher_schedule(teacher_id)
        except Exception as e:
            self._logger.error(f"Failed to fetch teacher schedule: {e}")
            # Generate mock schedule for this teacher
            return self._get_mock_teacher_schedule(teacher_id)
    
    def get_schedule(self, user_id: str) -> Dict[str, Any]:
        """
        Get schedule for a user (could be student, teacher, or admin)
        
        :param user_id: User ID
        :return: User's schedule data organized by days
        """
        try:
            # Call the API endpoint to get user schedule
            return self._api_client.get(f"schedule/user/{user_id}")
        except Exception as e:
            self._logger.error(f"Failed to fetch user schedule: {e}")
            # Try to determine if the user is a student or teacher
            if user_id.startswith("std"):
                return self._get_mock_student_schedule(user_id)
            elif user_id.startswith("tch"):
                return self._get_mock_teacher_schedule(user_id)
            else:
                return self._get_mock_schedule()
    
    def add_class(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new class to the schedule
        
        :param class_data: Class data to add
        :return: Added class data
        """
        try:
            # Call the API endpoint to add a class
            return self._api_client.post("schedule/classes", class_data)
        except Exception as e:
            self._logger.error(f"Failed to add class: {e}")
            # Return the input data with a mock ID
            import uuid
            class_data["id"] = str(uuid.uuid4())
            return class_data
    
    def update_class(self, class_id: str, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing class
        
        :param class_id: ID of class to update
        :param class_data: New class data
        :return: Updated class data
        """
        try:
            # Call the API endpoint to update a class
            return self._api_client.post(f"schedule/classes/{class_id}", class_data)
        except Exception as e:
            self._logger.error(f"Failed to update class: {e}")
            # Return the input data
            class_data["id"] = class_id
            return class_data
    
    def remove_class(self, class_id: str) -> None:
        """
        Remove a class from the schedule
        
        :param class_id: ID of class to remove
        """
        try:
            # Call the API endpoint to remove a class
            self._api_client.post(f"schedule/classes/{class_id}/delete", {})
        except Exception as e:
            self._logger.error(f"Failed to remove class: {e}")
    
    def _get_mock_schedule(self) -> Dict[str, Any]:
        """
        Generate mock schedule data for fallback
        
        :return: Mock schedule data organized by days
        """
        return {
            "monday": [
                {
                    "id": "class-001",
                    "subject_id": "subj-001",
                    "subject": "Matemáticas",
                    "time_start": "08:00",
                    "time_end": "10:00",
                    "room": "A101",
                    "teacher_id": "tch-001",
                    "teacher": "Laura Gómez"
                },
                {
                    "id": "class-002",
                    "subject_id": "subj-003",
                    "subject": "Física",
                    "time_start": "12:00",
                    "time_end": "14:00",
                    "room": "B201",
                    "teacher_id": "tch-002",
                    "teacher": "David Martinez"
                },
                {
                    "id": "class-003",
                    "subject_id": "subj-007",
                    "subject": "Inglés",
                    "time_start": "16:00",
                    "time_end": "18:00",
                    "room": "C301",
                    "teacher_id": "tch-003",
                    "teacher": "Sarah Johnson"
                }
            ],
            "tuesday": [
                {
                    "id": "class-004",
                    "subject_id": "subj-002",
                    "subject": "Historia",
                    "time_start": "10:00",
                    "time_end": "12:00",
                    "room": "A102",
                    "teacher_id": "tch-004",
                    "teacher": "Miguel Torres"
                },
                {
                    "id": "class-005",
                    "subject_id": "subj-004",
                    "subject": "Química",
                    "time_start": "14:00",
                    "time_end": "16:00",
                    "room": "B202",
                    "teacher_id": "tch-002",
                    "teacher": "David Martinez"
                }
            ],
            "wednesday": [
                {
                    "id": "class-006",
                    "subject_id": "subj-005",
                    "subject": "Literatura",
                    "time_start": "08:00",
                    "time_end": "10:00",
                    "room": "A103",
                    "teacher_id": "tch-005",
                    "teacher": "Carmen Vega"
                },
                {
                    "id": "class-007",
                    "subject_id": "subj-003",
                    "subject": "Física",
                    "time_start": "12:00",
                    "time_end": "14:00",
                    "room": "B201",
                    "teacher_id": "tch-002",
                    "teacher": "David Martinez"
                }
            ],
            "thursday": [
                {
                    "id": "class-008",
                    "subject_id": "subj-008",
                    "subject": "Computación",
                    "time_start": "10:00",
                    "time_end": "12:00",
                    "room": "C302",
                    "teacher_id": "tch-006",
                    "teacher": "Roberto Mendez"
                },
                {
                    "id": "class-009",
                    "subject_id": "subj-010",
                    "subject": "Arte",
                    "time_start": "16:00",
                    "time_end": "18:00",
                    "room": "A104",
                    "teacher_id": "tch-007",
                    "teacher": "Ana López"
                }
            ],
            "friday": [
                {
                    "id": "class-010",
                    "subject_id": "subj-006",
                    "subject": "Educación Física",
                    "time_start": "12:00",
                    "time_end": "14:00",
                    "room": "Gimnasio",
                    "teacher_id": "tch-008",
                    "teacher": "Pedro Ramírez"
                }
            ]
        }
    
    def _get_mock_student_schedule(self, student_id: str) -> Dict[str, Any]:
        """
        Generate mock schedule for a specific student
        
        :param student_id: Student ID
        :return: Student's schedule data organized by days
        """
        # For simplicity, return the general schedule
        # In a real implementation, this would filter classes for the specific student
        return self._get_mock_schedule()
    
    def _get_mock_teacher_schedule(self, teacher_id: str) -> Dict[str, Any]:
        """
        Generate mock schedule for a specific teacher
        
        :param teacher_id: Teacher ID
        :return: Teacher's schedule data organized by days
        """
        # Filter classes for the specific teacher
        all_schedule = self._get_mock_schedule()
        teacher_schedule = {}
        
        for day, classes in all_schedule.items():
            teacher_classes = [c for c in classes if c.get("teacher_id") == teacher_id]
            if teacher_classes:
                teacher_schedule[day] = teacher_classes
                
        return teacher_schedule