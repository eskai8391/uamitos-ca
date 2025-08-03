from typing import Callable, Dict, Optional, List
from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QTableWidgetItem, QCalendarWidget

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory


class EventsDetailsBuilder(Builder):
    """
    Builder for events details view that shows calendar and upcoming events
    """
    def __init__(
        self,
        wf: WidgetFactory,
        lf: LayoutFactory,
        on_back: Callable[[], None] = None
    ):
        """
        Initialize the events details builder
        
        :param wf: Widget factory
        :param lf: Layout factory
        :param on_back: Callback for back button
        """
        self._wf = wf
        self._lf = lf
        self._on_back = on_back or (lambda: None)
        
        # Create container
        self._container = QWidget()
        self._container.setObjectName("events-details-container")
        
        # Main layout using factory
        self._main_layout = self._lf.get("vbox").build()
        self._container.setLayout(self._main_layout)
        
        # Create components
        self._create_header()
        self._create_calendar_section()
        self._create_upcoming_events_section()
        
        # Apply styles
        self._apply_styles()
    
    def _create_header(self) -> None:
        """Create header with back button and title"""
        header = QFrame()
        header.setObjectName("details-header")
        
        # Use layout factory for header layout
        header_layout = self._lf.get("hbox").build()
        header.setLayout(header_layout)
        
        # Back button using widget factory
        self._back_button = self._wf.get("button").set_text("← Volver").build()
        self._back_button.setObjectName("back-button")
        self._back_button.clicked.connect(self._on_back)
        
        # Title using widget factory
        title = self._wf.get("label").set_text("Calendario de Eventos").build()
        title.setObjectName("details-title")
        
        # Add to layout
        header_layout.addWidget(self._back_button)
        header_layout.addWidget(title, 1, Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch(1)
        
        self._main_layout.addWidget(header)
    
    def _create_calendar_section(self) -> None:
        """Create calendar section"""
        calendar_frame = QFrame()
        calendar_frame.setObjectName("calendar-section")
        
        # Use layout factory
        calendar_layout = self._lf.get("vbox").build()
        calendar_frame.setLayout(calendar_layout)
        
        # Calendar widget
        self._calendar = QCalendarWidget()
        self._calendar.setObjectName("events-calendar")
        self._calendar.setMinimumHeight(300)
        self._calendar.selectionChanged.connect(self._handle_date_selected)
        
        # Add to layout
        calendar_layout.addWidget(self._calendar)
        
        self._main_layout.addWidget(calendar_frame)
    
    def _create_upcoming_events_section(self) -> None:
        """Create upcoming events section"""
        events_frame = QFrame()
        events_frame.setObjectName("events-list-section")
        
        # Use layout factory
        events_layout = self._lf.get("vbox").build()
        events_frame.setLayout(events_layout)
        
        # Section title using widget factory
        title = self._wf.get("label").set_text("Próximos Eventos").build()
        title.setObjectName("section-title")
        events_layout.addWidget(title)
        
        # Events table
        self._events_table = QTableWidget()
        self._events_table.setObjectName("events-table")
        self._events_table.setColumnCount(4)
        self._events_table.setHorizontalHeaderLabels(["Fecha", "Evento", "Hora", "Ubicación"])
        
        # Generate sample events
        current_date = datetime.now()
        events = []
        
        for i in range(10):
            event_date = current_date + timedelta(days=i)
            
            # Different events based on day of week
            if event_date.weekday() == 0:  # Monday
                events.append((
                    event_date.strftime("%Y-%m-%d"),
                    "Reunión de profesores",
                    "08:00 - 09:30",
                    "Sala de juntas"
                ))
            elif event_date.weekday() == 2:  # Wednesday
                events.append((
                    event_date.strftime("%Y-%m-%d"),
                    "Taller de matemáticas",
                    "12:00 - 14:00",
                    "Aula 101"
                ))
            elif event_date.weekday() == 4:  # Friday
                events.append((
                    event_date.strftime("%Y-%m-%d"),
                    "Clase especial de ciencias",
                    "10:00 - 11:30",
                    "Laboratorio"
                ))
        
        # Add some special events
        special_date = current_date + timedelta(days=5)
        events.append((
            special_date.strftime("%Y-%m-%d"),
            "Excursión de biología",
            "Todo el día",
            "Parque Nacional"
        ))
        
        special_date2 = current_date + timedelta(days=7)
        events.append((
            special_date2.strftime("%Y-%m-%d"),
            "Presentación de proyectos",
            "14:00 - 17:00",
            "Auditorio"
        ))
        
        # Filter out duplicates and sort by date
        unique_events = []
        seen_dates = set()
        
        for event in events:
            event_key = f"{event[0]}_{event[1]}"
            if event_key not in seen_dates:
                unique_events.append(event)
                seen_dates.add(event_key)
        
        # Sort by date
        unique_events.sort(key=lambda x: x[0])
        
        # Populate table
        self._events_table.setRowCount(len(unique_events))
        
        for row, (date, event, time, location) in enumerate(unique_events):
            self._events_table.setItem(row, 0, QTableWidgetItem(date))
            self._events_table.setItem(row, 1, QTableWidgetItem(event))
            self._events_table.setItem(row, 2, QTableWidgetItem(time))
            self._events_table.setItem(row, 3, QTableWidgetItem(location))
        
        # Connect double-click event
        self._events_table.cellDoubleClicked.connect(self._handle_event_selected)
        
        events_layout.addWidget(self._events_table)
        self._main_layout.addWidget(events_frame)
    
    def _handle_date_selected(self) -> None:
        """Handle date selection in calendar"""
        selected_date = self._calendar.selectedDate().toString("yyyy-MM-dd")
        print(f"Date selected: {selected_date}")
        
        # In a real implementation, you would filter events for the selected date
        # For now, we just print the selected date
        
        # Find events for selected date
        for row in range(self._events_table.rowCount()):
            event_date = self._events_table.item(row, 0).text()
            if event_date == selected_date:
                self._events_table.selectRow(row)
                return
        
        # If no events found, clear selection
        self._events_table.clearSelection()
    
    def _handle_event_selected(self, row: int, column: int) -> None:
        """Handle event selection from the table"""
        event_date = self._events_table.item(row, 0).text()
        event_title = self._events_table.item(row, 1).text()
        
        print(f"Event selected: {event_title} on {event_date}")
        # In a real implementation, you would show detailed information about the event
    
    def _apply_styles(self) -> None:
        """Apply styles to the components"""
        self._container.setStyleSheet("""
            #events-details-container {
                background-color: #f5f7fd;
                padding: 10px;
            }
            
            #details-header {
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }
            
            #back-button {
                background-color: transparent;
                border: none;
                color: #4a86e8;
                font-weight: bold;
            }
            
            #details-title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            
            #calendar-section {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            #events-calendar {
                background-color: white;
                selection-background-color: #8ecaef;
            }
            
            #events-list-section {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            #section-title {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            QTableWidget {
                border: none;
                background-color: white;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
            QTableWidget::item:selected {
                background-color: #e1f0ff;
            }
            
            QHeaderView::section {
                background-color: #d9d0c4;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def build(self) -> QWidget:
        """Build and return the events details widget"""
        return self._container
        
    def create(self):
        """Create a new instance of this builder"""
        return type(self)(
            self._wf,
            self._lf,
            self._on_back
        )
    
    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)