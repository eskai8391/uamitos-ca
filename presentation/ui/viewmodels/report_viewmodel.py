from typing import List, Dict, Any, Optional
import logging
from PySide6.QtCore import QObject, Signal

from infrastructure.api_client import ReportApiClient


class ReportViewModel(QObject):
    """ViewModel for handling report-related operations"""
    
    # Signals
    reportGenerated = Signal(dict)
    reportsLoaded = Signal(list)
    error = Signal(str)
    
    def __init__(self, api_client: ReportApiClient):
        """
        Initialize report view model
        
        :param api_client: Report API client
        """
        super().__init__()
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
        self._reports = []
        
        # Log API client state for debugging
        self._logger.info(f"ReportViewModel initialized with ReportApiClient instance: {id(api_client)}")
        if hasattr(api_client, "_api_client") and hasattr(api_client._api_client, "_token"):
            token = api_client._api_client._token
            self._logger.info(f"API token present: {bool(token)}")
        
    def load_reports(self) -> None:
        """Load reports from API"""
        try:
            self._logger.info("Loading reports")
            self._reports = self._api_client.get_reports()
                
            # Emit signal with loaded reports
            self.reportsLoaded.emit(self._reports)
        except Exception as e:
            error_msg = f"Failed to load reports: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            # Return empty list on error
            self._reports = []
            self.reportsLoaded.emit([])
            
    def get_reports(self) -> List[Dict[str, Any]]:
        """
        Get loaded reports
        
        :return: List of report data
        """
        return self._reports
        
    def generate_report(self, report_type: str, params: Optional[Dict[str, Any]] = None) -> None:
        """
        Generate a new report
        
        :param report_type: Type of report to generate
        :param params: Optional parameters for report generation
        """
        try:
            result = self._api_client.generate_report(report_type, params or {})
            self._logger.info(f"Generated report: {report_type}")
            self.reportGenerated.emit(result)
            # Reload reports to update the list
            self.load_reports()
        except Exception as e:
            error_msg = f"Failed to generate report: {str(e)}"
            self._logger.error(error_msg)
            self.error.emit(error_msg)
            
    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Find report by ID
        
        :param report_id: Report ID to find
        :return: Report data or None if not found
        """
        for report in self._reports:
            if report.get('id') == report_id or report.get('uuid') == report_id:
                return report
                
        try:
            # If not found in local cache, try to fetch from API
            return self._api_client.get_report_by_id(report_id)
        except Exception as e:
            self._logger.error(f"Failed to fetch report {report_id}: {e}")
            return None
            
    def download_report(self, report_id: str, output_path: str) -> bool:
        """
        Download report to file
        
        :param report_id: ID of report to download
        :param output_path: Path to save the report file
        :return: True if successful, False otherwise
        """
        try:
            result = self._api_client.download_report(report_id, output_path)
            self._logger.info(f"Downloaded report {report_id} to {output_path}")
            return result
        except Exception as e:
            self._logger.error(f"Failed to download report: {e}")
            self.error.emit(f"Failed to download report: {str(e)}")
            return False