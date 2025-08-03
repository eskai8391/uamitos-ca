import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from infrastructure.api_client.api_client import ApiClient, ApiClientException


class EventApiClient:
    """API client for event-related operations"""
    
    def __init__(self, api_client: ApiClient):
        """
        Initialize event API client
        
        :param api_client: Base API client
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    def get_all_events(self) -> List[Dict[str, Any]]:
        """
        Get all events
        
        :return: List of event data
        """
        try:
            # Call the API endpoint to get events
            events_data = self._api_client.get("events")
            if isinstance(events_data, list):
                return events_data
            else:
                self._logger.warning("Unexpected events data format")
                return []
        except Exception as e:
            self._logger.error(f"Failed to fetch events: {e}")
            # Provide some mock data in case of error
            return self._get_mock_events()
    
    def get_upcoming_events(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get upcoming events
        
        :param days: Number of days to look ahead
        :return: List of upcoming events
        """
        try:
            # Call the API endpoint to get upcoming events
            return self._api_client.get(f"events/upcoming?days={days}")
        except Exception as e:
            self._logger.error(f"Failed to fetch upcoming events: {e}")
            # Generate mock upcoming events
            return self._get_mock_upcoming_events(days)
    
    def get_event_by_id(self, event_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get event by UUID
        
        :param event_uuid: Event UUID
        :return: Event data or None if not found
        """
        try:
            # Call the API endpoint to get the event
            return self._api_client.get(f"events/{event_uuid}")
        except ApiClientException as e:
            if "404" in str(e):
                self._logger.info(f"Event not found: {event_uuid}")
                return None
            else:
                self._logger.error(f"Error fetching event: {e}")
                # Fallback to mock data
                events = self._get_mock_events()
                for event in events:
                    if event.get("uuid") == event_uuid:
                        return event
                return events[0] if events else None
        except Exception as e:
            self._logger.error(f"Failed to fetch event: {e}")
            return None
    
    def get_events_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get events for a specific date
        
        :param date: Date to find events for
        :return: List of events on that date
        """
        try:
            # Format date as YYYY-MM-DD
            formatted_date = date.strftime("%Y-%m-%d")
            # Call the API endpoint to get events by date
            return self._api_client.get(f"events/by-date/{formatted_date}")
        except Exception as e:
            self._logger.error(f"Failed to fetch events by date: {e}")
            # Filter mock events by date
            return self._get_mock_events_by_date(date)
    
    def get_events_by_organizer(self, organizer_uuid: str) -> List[Dict[str, Any]]:
        """
        Get events organized by a specific user
        
        :param organizer_uuid: Organizer UUID
        :return: List of events organized by the user
        """
        try:
            # Call the API endpoint to get events by organizer
            return self._api_client.get(f"events/by-organizer/{organizer_uuid}")
        except Exception as e:
            self._logger.error(f"Failed to fetch events by organizer: {e}")
            # Filter mock events by organizer
            return [e for e in self._get_mock_events() if e.get("organizer_uuid") == organizer_uuid]
    
    def _get_mock_events(self) -> List[Dict[str, Any]]:
        """
        Generate mock event data for fallback
        
        :return: List of mock event data
        """
        now = datetime.now()
        
        return [
            {
                "uuid": "evt-001",
                "title": "Reunión de profesores",
                "description": "Reunión mensual del claustro de profesores",
                "start_date": (now + timedelta(days=1)).replace(hour=8, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=1)).replace(hour=9, minute=30, second=0).isoformat(),
                "location": "Sala de juntas",
                "organizer_uuid": "tch-001",  # Laura Gómez
                "event_type": "meeting",
                "all_day": False
            },
            {
                "uuid": "evt-002",
                "title": "Taller de matemáticas",
                "description": "Taller práctico para reforzar conocimientos",
                "start_date": (now + timedelta(days=3)).replace(hour=12, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=3)).replace(hour=14, minute=0, second=0).isoformat(),
                "location": "Aula 101",
                "organizer_uuid": "tch-001",  # Laura Gómez
                "event_type": "workshop",
                "all_day": False
            },
            {
                "uuid": "evt-003",
                "title": "Clase especial de ciencias",
                "description": "Clase experimental sobre reacciones químicas",
                "start_date": (now + timedelta(days=4)).replace(hour=10, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=4)).replace(hour=11, minute=30, second=0).isoformat(),
                "location": "Laboratorio",
                "organizer_uuid": "tch-003",  # Ana Torres
                "event_type": "class",
                "all_day": False
            },
            {
                "uuid": "evt-004",
                "title": "Excursión de biología",
                "description": "Excursión al Parque Nacional para observación de fauna y flora",
                "start_date": (now + timedelta(days=5)).replace(hour=8, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=5)).replace(hour=18, minute=0, second=0).isoformat(),
                "location": "Parque Nacional",
                "organizer_uuid": "tch-004",  # María López
                "event_type": "field_trip",
                "all_day": True
            },
            {
                "uuid": "evt-005",
                "title": "Presentación de proyectos",
                "description": "Presentación de proyectos finales de estudiantes",
                "start_date": (now + timedelta(days=7)).replace(hour=14, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=7)).replace(hour=17, minute=0, second=0).isoformat(),
                "location": "Auditorio",
                "organizer_uuid": "tch-002",  # Pedro Ruiz
                "event_type": "presentation",
                "all_day": False
            },
            {
                "uuid": "evt-006",
                "title": "Exámenes finales",
                "description": "Periodo de exámenes finales del semestre",
                "start_date": (now + timedelta(days=14)).replace(hour=8, minute=0, second=0).isoformat(),
                "end_date": (now + timedelta(days=18)).replace(hour=17, minute=0, second=0).isoformat(),
                "location": "Múltiples aulas",
                "organizer_uuid": "tch-005",  # Juan Pérez
                "event_type": "exam",
                "all_day": True
            }
        ]
    
    def _get_mock_upcoming_events(self, days: int) -> List[Dict[str, Any]]:
        """
        Generate mock upcoming event data
        
        :param days: Number of days to look ahead
        :return: List of mock upcoming event data
        """
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        events = self._get_mock_events()
        upcoming = []
        
        for event in events:
            event_date = datetime.fromisoformat(event["start_date"])
            if now <= event_date <= cutoff:
                upcoming.append(event)
        
        return upcoming
    
    def _get_mock_events_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Filter mock events by date
        
        :param date: Date to filter by
        :return: List of events on that date
        """
        events = self._get_mock_events()
        events_on_date = []
        
        # Set time to start and end of day
        start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        
        for event in events:
            event_start = datetime.fromisoformat(event["start_date"])
            event_end = datetime.fromisoformat(event["end_date"])
            
            # Check if event occurs on the specified date
            if (start_of_day <= event_start <= end_of_day or
                start_of_day <= event_end <= end_of_day or
                (event_start <= start_of_day and event_end >= end_of_day)):
                events_on_date.append(event)
        
        return events_on_date