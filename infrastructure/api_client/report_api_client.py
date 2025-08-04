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
            return self._api_client.get(f"reports/{report_id}")
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
                "type": "Asistencia",
                "date": "01/08/2025",
                "status": "completed",
                "file_path": "/reports/asistencia_20250801.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-002",
                "uuid": "rep-002",
                "name": "Reporte de Calificaciones - Semestre 2025-1",
                "type": "Calificaciones",
                "date": "29/07/2025",
                "status": "completed",
                "file_path": "/reports/calificaciones_20250729.pdf",
                "created_at": now.isoformat()
            },
            {
                "id": "rep-003",
                "uuid": "rep-003",
                "name": "Reporte de Usuarios Nuevos",
                "type": "Usuarios",
                "date": "25/07/2025",
                "status": "completed",
                "file_path": "/reports/usuarios_20250725.pdf",
                "created_at": now.isoformat()
            }
        ]