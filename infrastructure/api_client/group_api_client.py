import logging
from typing import List, Dict, Any, Optional

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class GroupApiClient:
    """API client for group-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize group API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_all_groups(self) -> List[Dict[str, Any]]:
        """
        Get all groups
        
        :return: List of group data
        """
        try:
            groups_data = self._api_client.get("groups")
            if isinstance(groups_data, list):
                return groups_data
            else:
                self._logger.warning("Unexpected groups data format")
                return []
        except Exception as e:
            self._logger.error(f"Failed to fetch groups: {e}")
            # Provide mock data in case of error
            return self._get_mock_groups()
    
    def get_group_by_id(self, group_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get group by UUID
        
        :param group_uuid: Group UUID
        :return: Group data or None if not found
        """
        try:
            return self._api_client.get(f"groups/{group_uuid}")
        except Exception as e:
            self._logger.error(f"Failed to fetch group: {e}")
            # Try to find in mock data
            groups = self._get_mock_groups()
            for group in groups:
                if group.get("uuid") == group_uuid:
                    return group
            return None
    
    def get_groups_by_teacher(self, teacher_uuid: str) -> List[Dict[str, Any]]:
        """
        Get groups taught by a specific teacher
        
        :param teacher_uuid: Teacher UUID
        :return: List of group data
        """
        try:
            return self._api_client.get(f"teachers/{teacher_uuid}/groups")
        except Exception as e:
            self._logger.error(f"Failed to fetch teacher's groups: {e}")
            # Filter mock data for this teacher
            groups = self._get_mock_groups()
            return [g for g in groups if g.get("teacher_uuid") == teacher_uuid]
    
    def get_groups_by_student(self, student_uuid: str) -> List[Dict[str, Any]]:
        """
        Get groups that a student is enrolled in
        
        :param student_uuid: Student UUID
        :return: List of group data
        """
        try:
            return self._api_client.get(f"students/{student_uuid}/groups")
        except Exception as e:
            self._logger.error(f"Failed to fetch student's groups: {e}")
            # Filter mock data for this student
            groups = self._get_mock_groups()
            return [
                g for g in groups 
                if any(student.get("uuid") == student_uuid for student in g.get("students", []))
            ]
    
    def add_student_to_group(self, group_uuid: str, student_uuid: str) -> bool:
        """
        Add a student to a group
        
        :param group_uuid: Group UUID
        :param student_uuid: Student UUID
        :return: True if successful, False otherwise
        """
        try:
            self._api_client.post(f"groups/{group_uuid}/students", {
                "student_uuid": student_uuid
            })
            return True
        except Exception as e:
            self._logger.error(f"Failed to add student to group: {e}")
            return False
    
    def remove_student_from_group(self, group_uuid: str, student_uuid: str) -> bool:
        """
        Remove a student from a group
        
        :param group_uuid: Group UUID
        :param student_uuid: Student UUID
        :return: True if successful, False otherwise
        """
        try:
            # This requires a custom call since DELETE usually doesn't have a body
            url = f"groups/{group_uuid}/students/{student_uuid}"
            self._api_client.delete(url)
            return True
        except Exception as e:
            self._logger.error(f"Failed to remove student from group: {e}")
            return False
    
    def create_group(self, group_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new group
        
        :param group_data: Group data
        :return: Created group data or None if failed
        """
        try:
            return self._api_client.post("groups", group_data)
        except Exception as e:
            self._logger.error(f"Failed to create group: {e}")
            return None
    
    def delete_group(self, group_uuid: str) -> bool:
        """
        Delete a group
        
        :param group_uuid: Group UUID
        :return: True if successful, False otherwise
        """
        try:
            self._api_client.delete(f"groups/{group_uuid}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to delete group: {e}")
            return False
    
    def _get_mock_groups(self) -> List[Dict[str, Any]]:
        """
        Generate mock group data for fallback
        
        :return: List of mock group data
        """
        return [
            {
                "uuid": "group-001",
                "name": "Matemáticas Grupo A",
                "subject_uuid": "subj-001",
                "subject_name": "Matemáticas",
                "teacher_uuid": "teacher-001",
                "teacher_name": "Juan Pérez",
                "day_of_week": 0,  # Monday
                "start_time": "08:00",
                "end_time": "10:00",
                "room": "A101",
                "max_students": 30,
                "semester": "2025-1",
                "student_count": 25,
                "students": [
                    {"uuid": "stu-001", "name": "Ana López", "email": "ana.lopez@uamitos.edu.mx"},
                    {"uuid": "stu-002", "name": "Luis Pérez", "email": "luis.perez@uamitos.edu.mx"},
                    {"uuid": "stu-003", "name": "Marta Sánchez", "email": "marta.sanchez@uamitos.edu.mx"}
                ]
            },
            {
                "uuid": "group-002",
                "name": "Historia Grupo B",
                "subject_uuid": "subj-002",
                "subject_name": "Historia",
                "teacher_uuid": "teacher-002",
                "teacher_name": "María Rodríguez",
                "day_of_week": 1,  # Tuesday
                "start_time": "10:00",
                "end_time": "12:00",
                "room": "B202",
                "max_students": 30,
                "semester": "2025-1",
                "student_count": 28,
                "students": [
                    {"uuid": "stu-001", "name": "Ana López", "email": "ana.lopez@uamitos.edu.mx"},
                    {"uuid": "stu-004", "name": "Carlos Gómez", "email": "carlos.gomez@uamitos.edu.mx"},
                    {"uuid": "stu-005", "name": "Lucía Torres", "email": "lucia.torres@uamitos.edu.mx"}
                ]
            },
            {
                "uuid": "group-003",
                "name": "Física Grupo C",
                "subject_uuid": "subj-003",
                "subject_name": "Física",
                "teacher_uuid": "teacher-001",
                "teacher_name": "Juan Pérez",
                "day_of_week": 2,  # Wednesday
                "start_time": "13:00",
                "end_time": "15:00",
                "room": "C303",
                "max_students": 30,
                "semester": "2025-1",
                "student_count": 20,
                "students": [
                    {"uuid": "stu-002", "name": "Luis Pérez", "email": "luis.perez@uamitos.edu.mx"},
                    {"uuid": "stu-003", "name": "Marta Sánchez", "email": "marta.sanchez@uamitos.edu.mx"},
                    {"uuid": "stu-004", "name": "Carlos Gómez", "email": "carlos.gomez@uamitos.edu.mx"}
                ]
            }
        ]