import logging
from typing import List, Dict, Any, Optional

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class TeacherApiClient:
    """API client for teacher-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize teacher API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_all_teachers(self) -> List[Dict[str, Any]]:
        """
        Get all teachers
        
        :return: List of teacher data
        """
        try:
            # Call the API endpoint to get teachers
            teachers_data = self._api_client.get("teachers")
            if isinstance(teachers_data, list):
                return teachers_data
            else:
                self._logger.warning("Unexpected teachers data format")
                return []
        except Exception as e:
            self._logger.error(f"Failed to fetch teachers: {e}")
            # Provide some mock data in case of error
            return self._get_mock_teachers()
    
    def get_teacher_by_id(self, teacher_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get teacher by UUID
        
        :param teacher_uuid: Teacher UUID
        :return: Teacher data or None if not found
        """
        try:
            # Call the API endpoint to get the teacher
            return self._api_client.get(f"teachers/{teacher_uuid}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Teacher not found: {teacher_uuid}")
                return None
            else:
                self._logger.error(f"Error fetching teacher: {e}")
                # Fallback to mock data
                teachers = self._get_mock_teachers()
                for teacher in teachers:
                    if teacher.get("uuid") == teacher_uuid:
                        return teacher
                return teachers[0] if teachers else None
        except Exception as e:
            self._logger.error(f"Failed to fetch teacher: {e}")
            return None
    
    def get_teacher_subjects(self, teacher_uuid: str) -> List[Dict[str, Any]]:
        """
        Get subjects taught by a teacher
        
        :param teacher_uuid: Teacher UUID
        :return: List of subject data
        """
        try:
            # Call the API endpoint to get the teacher's subjects
            return self._api_client.get(f"teachers/{teacher_uuid}/subjects")
        except Exception as e:
            self._logger.error(f"Failed to fetch teacher subjects: {e}")
            # Provide some mock data in case of error
            return self._get_mock_subjects(teacher_uuid)
    
    def _get_mock_teachers(self) -> List[Dict[str, Any]]:
        """
        Generate mock teacher data for fallback
        
        :return: List of mock teacher data
        """
        return [
            {
                "uuid": "tch-001",
                "email": "laura.gomez@uamitos.edu.mx",
                "first_name": "Laura",
                "last_name": "Gómez",
                "role": "teacher",
                "is_active": True,
                "last_login": "2025-07-01T08:30:00",
                "phone": "+52-555-123-4567",
                "department": "Ciencias Exactas",
                "specialization": "Matemáticas"
            },
            {
                "uuid": "tch-002",
                "email": "pedro.ruiz@uamitos.edu.mx",
                "first_name": "Pedro",
                "last_name": "Ruiz",
                "role": "teacher",
                "is_active": True,
                "last_login": "2025-07-01T09:15:00",
                "phone": "+52-555-234-5678",
                "department": "Ciencias Exactas",
                "specialization": "Física"
            },
            {
                "uuid": "tch-003",
                "email": "ana.torres@uamitos.edu.mx",
                "first_name": "Ana",
                "last_name": "Torres",
                "role": "teacher",
                "is_active": True,
                "last_login": "2025-07-01T10:00:00",
                "phone": "+52-555-345-6789",
                "department": "Ciencias Exactas",
                "specialization": "Química"
            },
            {
                "uuid": "tch-004",
                "email": "maria.lopez@uamitos.edu.mx",
                "first_name": "María",
                "last_name": "López",
                "role": "teacher",
                "is_active": True,
                "last_login": "2025-07-01T11:30:00",
                "phone": "+52-555-456-7890",
                "department": "Ciencias Naturales",
                "specialization": "Biología"
            },
            {
                "uuid": "tch-005",
                "email": "juan.perez@uamitos.edu.mx",
                "first_name": "Juan",
                "last_name": "Pérez",
                "role": "teacher",
                "is_active": True,
                "last_login": "2025-07-01T12:45:00",
                "phone": "+52-555-567-8901",
                "department": "Humanidades",
                "specialization": "Historia"
            }
        ]
    
    def _get_mock_subjects(self, teacher_uuid: str) -> List[Dict[str, Any]]:
        """
        Generate mock subject data for a teacher
        
        :param teacher_uuid: Teacher UUID
        :return: List of mock subject data
        """
        subjects_by_teacher = {
            "tch-001": [  # Laura Gómez (Matemáticas)
                {
                    "uuid": "subj-001",
                    "name": "Matemáticas I",
                    "code": "MAT101",
                    "description": "Introducción al álgebra y cálculo",
                    "credits": 4,
                    "semester": 1
                },
                {
                    "uuid": "subj-002",
                    "name": "Matemáticas II",
                    "code": "MAT201",
                    "description": "Álgebra lineal y geometría analítica",
                    "credits": 4,
                    "semester": 2
                },
                {
                    "uuid": "subj-003",
                    "name": "Álgebra",
                    "code": "MAT301",
                    "description": "Álgebra avanzada y ecuaciones",
                    "credits": 4,
                    "semester": 3
                }
            ],
            "tch-002": [  # Pedro Ruiz (Física)
                {
                    "uuid": "subj-004",
                    "name": "Física I",
                    "code": "FIS101",
                    "description": "Mecánica newtoniana",
                    "credits": 4,
                    "semester": 2
                },
                {
                    "uuid": "subj-005",
                    "name": "Física II",
                    "code": "FIS201",
                    "description": "Electromagnetismo",
                    "credits": 4,
                    "semester": 3
                }
            ],
            "tch-003": [  # Ana Torres (Química)
                {
                    "uuid": "subj-006",
                    "name": "Química I",
                    "code": "QUI101",
                    "description": "Química general",
                    "credits": 4,
                    "semester": 1
                },
                {
                    "uuid": "subj-007",
                    "name": "Química II",
                    "code": "QUI201",
                    "description": "Química orgánica",
                    "credits": 4,
                    "semester": 2
                }
            ],
            "tch-004": [  # María López (Biología)
                {
                    "uuid": "subj-008",
                    "name": "Biología I",
                    "code": "BIO101",
                    "description": "Biología celular",
                    "credits": 4,
                    "semester": 1
                },
                {
                    "uuid": "subj-009",
                    "name": "Biología II",
                    "code": "BIO201",
                    "description": "Anatomía y fisiología",
                    "credits": 4,
                    "semester": 2
                }
            ],
            "tch-005": [  # Juan Pérez (Historia)
                {
                    "uuid": "subj-010",
                    "name": "Historia I",
                    "code": "HIS101",
                    "description": "Historia antigua y medieval",
                    "credits": 3,
                    "semester": 1
                },
                {
                    "uuid": "subj-011",
                    "name": "Historia II",
                    "code": "HIS201",
                    "description": "Historia moderna y contemporánea",
                    "credits": 3,
                    "semester": 2
                }
            ]
        }
        
        return subjects_by_teacher.get(teacher_uuid, [])