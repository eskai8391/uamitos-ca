import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer

from infrastructure.api_client import EventApiClient


class EventViewModel(QObject):
    """
    View model for event-related data
    Handles fetching and processing event data from API
    """
    
    # Signals
    eventsLoaded = Signal(list)  # List of event data
    upcomingEventsLoaded = Signal(list)  # List of upcoming events
    eventDetailsLoaded = Signal(dict)  # Event details
    eventsByDateLoaded = Signal(list)  # Events for a specific date
    monthlyAttendanceLoaded = Signal(dict)  # Monthly attendance data
    error = Signal(str)  # Error message
    
    def __init__(self, event_api_client: EventApiClient, parent: Optional[QObject] = None):
        """
        Initialize the event view model
        
        :param event_api_client: EventApiClient instance
        :param parent: Parent QObject
        """
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._api_client = event_api_client
        
        # Properties
        self._events = []
        self._upcoming_events = []
        self._current_event = None
        self._events_by_date = {}
        self._monthly_attendance = {}
        self._is_loading = False
        
        # Setup auto-refresh timer (refresh every 5 minutes)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.load_upcoming_events)
        self._refresh_timer.start(300000)  # 5 minutes
    
    @Property(bool)
    def is_loading(self) -> bool:
        return self._is_loading
    
    @is_loading.setter
    def is_loading(self, value: bool) -> None:
        if self._is_loading != value:
            self._is_loading = value
    
    @Property(list)
    def events(self) -> List[Dict[str, Any]]:
        return self._events
    
    @Property(list)
    def upcoming_events(self) -> List[Dict[str, Any]]:
        return self._upcoming_events
    
    @Property(dict)
    def current_event(self) -> Optional[Dict[str, Any]]:
        return self._current_event
    
    @Slot()
    def load_all_events(self) -> None:
        """Load all events"""
        self._logger.info("Loading all events")
        self.is_loading = True
        
        try:
            events = self._api_client.get_all_events()
            self._events = events
            self.eventsLoaded.emit(events)
            self._logger.info(f"Loaded {len(events)} events")
        except Exception as e:
            self._logger.error(f"Error loading events: {e}")
            self.error.emit(f"Error loading events: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(int)
    def load_upcoming_events(self, days: int = 30) -> None:
        """
        Load upcoming events within a specified number of days
        
        :param days: Number of days to look ahead
        """
        self._logger.info(f"Loading upcoming events for the next {days} days")
        self.is_loading = True
        
        try:
            events = self._api_client.get_upcoming_events(days)
            self._upcoming_events = events
            self.upcomingEventsLoaded.emit(events)
            self._logger.info(f"Loaded {len(events)} upcoming events")
        except Exception as e:
            self._logger.error(f"Error loading upcoming events: {e}")
            self.error.emit(f"Error loading upcoming events: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_event_details(self, event_uuid: str) -> None:
        """
        Load details for a specific event
        
        :param event_uuid: Event UUID
        """
        self._logger.info(f"Loading event details for {event_uuid}")
        self.is_loading = True
        
        try:
            event = self._api_client.get_event_by_id(event_uuid)
            if event:
                self._current_event = event
                self.eventDetailsLoaded.emit(event)
                self._logger.info(f"Loaded details for event {event_uuid}")
            else:
                self._logger.warning(f"Event {event_uuid} not found")
                self.error.emit(f"Event not found")
        except Exception as e:
            self._logger.error(f"Error loading event details: {e}")
            self.error.emit(f"Error loading event details: {str(e)}")
        finally:
            self.is_loading = False
    
    @Slot(str)
    def load_events_by_date(self, date_str: str) -> None:
        """
        Load events for a specific date
        
        :param date_str: Date string in 'YYYY-MM-DD' format
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            self._logger.info(f"Loading events for date: {date_str}")
            self.is_loading = True
            
            events = self._api_client.get_events_by_date(date)
            self._events_by_date[date_str] = events
            self.eventsByDateLoaded.emit(events)
            self._logger.info(f"Loaded {len(events)} events for {date_str}")
        except ValueError:
            self._logger.error(f"Invalid date format: {date_str}")
            self.error.emit("Invalid date format. Use 'YYYY-MM-DD'.")
        except Exception as e:
            self._logger.error(f"Error loading events by date: {e}")
            self.error.emit(f"Error loading events: {str(e)}")
        finally:
            self.is_loading = False
    
    def format_upcoming_events_for_display(self) -> List[tuple]:
        """
        Format upcoming events for display in a list
        
        :return: List of tuples with (date, title, time, days_left)
        """
        result = []
        now = datetime.now()
        
        for event in self._upcoming_events:
            try:
                # Parse date and time
                start_date = datetime.fromisoformat(event.get('start_date'))
                title = event.get('title')
                
                # Format time string
                if event.get('all_day', False):
                    time_str = "Todo el día"
                else:
                    end_date = datetime.fromisoformat(event.get('end_date'))
                    time_str = f"{start_date.strftime('%H:%M')} - {end_date.strftime('%H:%M')}"
                
                # Calculate days left
                days_diff = (start_date.date() - now.date()).days
                if days_diff == 0:
                    days_left = "Hoy"
                elif days_diff == 1:
                    days_left = "Mañana"
                else:
                    days_left = f"En {days_diff} días"
                
                # Format weekday and date
                weekday = start_date.strftime("%A")
                weekday_es = {
                    "Monday": "Lunes",
                    "Tuesday": "Martes",
                    "Wednesday": "Miércoles",
                    "Thursday": "Jueves",
                    "Friday": "Viernes",
                    "Saturday": "Sábado",
                    "Sunday": "Domingo"
                }.get(weekday, weekday)
                
                date_str = start_date.strftime("%d")
                
                result.append((weekday_es, date_str, title, time_str, days_left))
            except (ValueError, TypeError) as e:
                self._logger.warning(f"Error formatting event: {e}")
        
        return result
    
    @Slot(int)
    def load_monthly_attendance(self, months: int = 5) -> None:
        """
        Load monthly attendance data
        
        :param months: Number of months to retrieve
        """
        self._logger.info(f"Loading monthly attendance data for the last {months} months")
        self.is_loading = True
        
        try:
            attendance_data = self._api_client.get_monthly_attendance(months)
            self._monthly_attendance = attendance_data
            self.monthlyAttendanceLoaded.emit(attendance_data)
            self._logger.info(f"Loaded monthly attendance data: {attendance_data}")
        except Exception as e:
            self._logger.error(f"Error loading monthly attendance: {e}")
            self.error.emit(f"Error loading monthly attendance: {str(e)}")
        finally:
            self.is_loading = False
    
    def dispose(self) -> None:
        """Clean up resources"""
        self._refresh_timer.stop()