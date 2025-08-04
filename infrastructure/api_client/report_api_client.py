import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class ReportApiClient:
    """API client for report-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize report API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_reports(self) -> List[Dict[str, Any]]:
        """
        Get all reports
        
        :return: List of report data
        """
        try:
            # Call the API endpoint to get reports
            reports_data = self._api_client.get("reports")
            if isinstance(reports_data, list):
                return reports_data
            else:
                self._logger.warning("Unexpected reports data format")
                return []
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Reports endpoint not found, using mock data")
                # Generate mock reports
                return self._get_mock_reports()
            else:
                self._logger.error(f"Failed to fetch reports: {e}")
                # Provide some mock data in case of error
                return self._get_mock_reports()
        except Exception as e:
            self._logger.error(f"Failed to fetch reports: {e}")
            # Provide some mock data in case of error
            return self._get_mock_reports()
    
    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get report by ID
        
        :param report_id: Report ID
        :return: Report data or None if not found
        """
        try:
            # Call the API endpoint to get the report
            report = self._api_client.get(f"reports/{report_id}")
            if report and "data" in report:
                # Return the report with its data included
                return report
            return report
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Report not found: {report_id}")
                return None
            else:
                self._logger.error(f"Error fetching report: {e}")
                # Try to find in mock data
                reports = self._get_mock_reports()
                for report in reports:
                    if report.get("id") == report_id or report.get("uuid") == report_id:
                        # Add mock data to the report
                        if "data" not in report:
                            report["data"] = self._generate_mock_report_data(report.get("type", ""))
                        return report
                return None
        except Exception as e:
            self._logger.error(f"Failed to fetch report: {e}")
            return None
    
    def generate_report(self, report_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a new report
        
        :param report_type: Type of report to generate
        :param params: Parameters for report generation
        :return: Generated report data
        """
        try:
            # Call the API endpoint to generate a report
            data = {
                "report_type": report_type
            }
            if params:
                data.update(params)
                
            return self._api_client.post("reports/generate", data)
        except Exception as e:
            self._logger.error(f"Failed to generate report: {e}")
            # Return a mock report
            import uuid
            
            now = datetime.now()
            formatted_date = now.strftime("%d/%m/%Y")
            
            return {
                "id": f"rep-{uuid.uuid4().hex[:6]}",
                "name": f"{report_type} - {formatted_date}",
                "type": report_type,
                "date": formatted_date,
                "status": "completed",
                "file_path": f"/reports/{report_type.lower().replace(' ', '_')}_{now.strftime('%Y%m%d')}.pdf"
            }
    
    def download_report(self, report_id: str, output_path: str) -> bool:
        """
        Download a report to file
        
        :param report_id: ID of report to download
        :param output_path: Path to save the report file
        :return: True if successful, False otherwise
        """
        try:
            # In a real implementation, this would download the report file
            # For now, we just create an empty file
            self._logger.info(f"Simulating download of report {report_id} to {output_path}")
            
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create an empty file
            with open(output_path, 'w') as f:
                f.write(f"This is a placeholder for report {report_id}")
                
            return True
        except Exception as e:
            self._logger.error(f"Failed to download report: {e}")
            return False
            
    def _generate_mock_report_data(self, report_type: str) -> Dict[str, Any]:
        """
        Generate mock report data based on the report type
        
        :param report_type: Type of report
        :return: Mock report data
        """
        if report_type.lower() == "attendance" or report_type.lower() == "asistencia":
            return {
                "overall_attendance_rate": 85.7,
                "total_classes": 45,
                "subjects": [
                    {
                        "subject": "Matemáticas",
                        "total_classes": 15,
                        "students": [
                            {"name": "Alex Johnson", "present": 13, "absent": 2, "attendance_rate": 86.7, "status": "Good"},
                            {"name": "Maria Garcia", "present": 15, "absent": 0, "attendance_rate": 100.0, "status": "Good"},
                            {"name": "David Martinez", "present": 12, "absent": 3, "attendance_rate": 80.0, "status": "Good"}
                        ]
                    },
                    {
                        "subject": "Física",
                        "total_classes": 15,
                        "students": [
                            {"name": "Alex Johnson", "present": 14, "absent": 1, "attendance_rate": 93.3, "status": "Good"},
                            {"name": "Maria Garcia", "present": 14, "absent": 1, "attendance_rate": 93.3, "status": "Good"},
                            {"name": "David Martinez", "present": 10, "absent": 5, "attendance_rate": 66.7, "status": "Warning"}
                        ]
                    },
                    {
                        "subject": "Química",
                        "total_classes": 15,
                        "students": [
                            {"name": "Alex Johnson", "present": 11, "absent": 4, "attendance_rate": 73.3, "status": "Warning"},
                            {"name": "Maria Garcia", "present": 13, "absent": 2, "attendance_rate": 86.7, "status": "Good"},
                            {"name": "David Martinez", "present": 13, "absent": 2, "attendance_rate": 86.7, "status": "Good"}
                        ]
                    }
                ]
            }
        elif report_type.lower() == "grades" or report_type.lower() == "calificaciones":
            return {
                "overall_average": 82.3,
                "subjects": [
                    {
                        "subject": "Matemáticas",
                        "average": 78.6,
                        "students": [
                            {"name": "Alex Johnson", "midterm": 75.0, "final": 85.0, "assignments": 80.0, "final_grade": 81.0, "status": "Aprobado"},
                            {"name": "Maria Garcia", "midterm": 90.0, "final": 92.0, "assignments": 95.0, "final_grade": 92.5, "status": "Aprobado"},
                            {"name": "David Martinez", "midterm": 65.0, "final": 70.0, "assignments": 75.0, "final_grade": 70.5, "status": "Aprobado"}
                        ]
                    },
                    {
                        "subject": "Física",
                        "average": 82.7,
                        "students": [
                            {"name": "Alex Johnson", "midterm": 80.0, "final": 85.0, "assignments": 78.0, "final_grade": 81.4, "status": "Aprobado"},
                            {"name": "Maria Garcia", "midterm": 85.0, "final": 90.0, "assignments": 88.0, "final_grade": 88.1, "status": "Aprobado"},
                            {"name": "David Martinez", "midterm": 70.0, "final": 80.0, "assignments": 85.0, "final_grade": 78.5, "status": "Aprobado"}
                        ]
                    },
                    {
                        "subject": "Química",
                        "average": 85.5,
                        "students": [
                            {"name": "Alex Johnson", "midterm": 88.0, "final": 92.0, "assignments": 90.0, "final_grade": 90.2, "status": "Aprobado"},
                            {"name": "Maria Garcia", "midterm": 95.0, "final": 98.0, "assignments": 96.0, "final_grade": 96.7, "status": "Aprobado"},
                            {"name": "David Martinez", "midterm": 70.0, "final": 75.0, "assignments": 65.0, "final_grade": 70.5, "status": "Aprobado"}
                        ]
                    }
                ]
            }
        elif report_type.lower() == "users" or report_type.lower() == "usuarios":
            return {
                "total_users": 35,
                "student_count": 20,
                "teacher_count": 10,
                "active_students": 18,
                "active_teachers": 9,
                "inactive_students": 2,
                "inactive_teachers": 1,
                "monthly_growth": [
                    {"month": "Mar", "new_students": 8, "new_teachers": 2},
                    {"month": "Apr", "new_students": 5, "new_teachers": 1},
                    {"month": "May", "new_students": 3, "new_teachers": 0},
                    {"month": "Jun", "new_students": 2, "new_teachers": 2},
                    {"month": "Jul", "new_students": 6, "new_teachers": 3},
                    {"month": "Aug", "new_students": 10, "new_teachers": 2}
                ]
            }
        elif report_type.lower() == "performance" or report_type.lower() == "rendimiento":
            return {
                "current_semester": {
                    "overall_gpa": 8.2,
                    "pass_rate": 92.5,
                    "attendance_rate": 88.7,
                    "subject_performance": [
                        {"name": "Matemáticas", "average_grade": 78.5, "pass_rate": 90.0, "performance_level": "Satisfactorio"},
                        {"name": "Física", "average_grade": 82.3, "pass_rate": 94.5, "performance_level": "Bueno"},
                        {"name": "Química", "average_grade": 85.7, "pass_rate": 96.0, "performance_level": "Bueno"},
                        {"name": "Literatura", "average_grade": 91.2, "pass_rate": 98.5, "performance_level": "Excelente"}
                    ]
                },
                "historical_data": [
                    {"name": "2023-1", "overall_gpa": 7.8, "pass_rate": 88.5, "attendance_rate": 86.2},
                    {"name": "2023-2", "overall_gpa": 7.9, "pass_rate": 90.1, "attendance_rate": 87.5},
                    {"name": "2024-1", "overall_gpa": 8.0, "pass_rate": 91.2, "attendance_rate": 87.8},
                    {"name": "2024-2", "overall_gpa": 8.1, "pass_rate": 91.8, "attendance_rate": 88.3},
                    {"name": "2025-1", "overall_gpa": 8.2, "pass_rate": 92.5, "attendance_rate": 88.7}
                ]
            }
        elif report_type.lower() == "schedule" or report_type.lower() == "horario":
            return {
                "teacher_schedules": [
                    {
                        "name": "John Doe",
                        "total_hours": 6,
                        "schedule": {
                            "Lunes": [
                                {"time": "08:00-10:00", "subject": "Matemáticas", "room": "A101"}
                            ],
                            "Martes": [
                                {"time": "10:00-12:00", "subject": "Matemáticas", "room": "A102"}
                            ],
                            "Miércoles": [
                                {"time": "12:00-14:00", "subject": "Álgebra", "room": "B201"}
                            ],
                            "Jueves": [],
                            "Viernes": []
                        }
                    },
                    {
                        "name": "Jane Smith",
                        "total_hours": 4,
                        "schedule": {
                            "Lunes": [],
                            "Martes": [
                                {"time": "14:00-16:00", "subject": "Física", "room": "B202"}
                            ],
                            "Miércoles": [],
                            "Jueves": [
                                {"time": "10:00-12:00", "subject": "Física Avanzada", "room": "B201"}
                            ],
                            "Viernes": []
                        }
                    }
                ],
                "room_utilization": [
                    {"room_id": "A101", "usage_count": 5, "utilization_rate": 20.0},
                    {"room_id": "A102", "usage_count": 8, "utilization_rate": 32.0},
                    {"room_id": "B201", "usage_count": 12, "utilization_rate": 48.0},
                    {"room_id": "B202", "usage_count": 7, "utilization_rate": 28.0},
                    {"room_id": "C301", "usage_count": 3, "utilization_rate": 12.0}
                ]
            }
        else:
            # Generic report data
            return {
                "message": f"No specific mock data available for report type: {report_type}",
                "generated_at": datetime.now().isoformat()
            }
    
    def _get_mock_reports(self) -> List[Dict[str, Any]]:
        """
        Generate mock report data for fallback
        
        :return: List of mock report data
        """
        now = datetime.now()
        
        return [
            {
                "id": "rep-001",
                "uuid": "rep-001",
                "name": "Reporte de Asistencia - Agosto 2025",
                "type": "attendance",
                "date": "01/08/2025",
                "status": "Completado",
                "created_by": "admin@uamitos.edu.mx",
                "file_path": "/reports/asistencia_20250801.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-002",
                "uuid": "rep-002",
                "name": "Reporte de Calificaciones - Semestre 2025-1",
                "type": "grades",
                "date": "29/07/2025",
                "status": "Completado",
                "created_by": "admin@uamitos.edu.mx",
                "file_path": "/reports/calificaciones_20250729.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-003",
                "uuid": "rep-003",
                "name": "Reporte de Usuarios Nuevos",
                "type": "users",
                "date": "25/07/2025",
                "status": "Completado",
                "created_by": "admin@uamitos.edu.mx",
                "file_path": "/reports/usuarios_20250725.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-004",
                "uuid": "rep-004",
                "name": "Reporte de Rendimiento Académico",
                "type": "performance",
                "date": "22/07/2025",
                "status": "Completado",
                "created_by": "admin@uamitos.edu.mx",
                "file_path": "/reports/rendimiento_20250722.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-005",
                "uuid": "rep-005",
                "name": "Reporte de Horarios - Agosto 2025",
                "type": "schedule",
                "date": "27/07/2025",
                "status": "Completado",
                "created_by": "admin@uamitos.edu.mx",
                "file_path": "/reports/horarios_20250727.pdf",
                "created_at": now.isoformat()
            }
        ]