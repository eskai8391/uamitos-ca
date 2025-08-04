import logging
from typing import Callable, Dict, Optional, List, Tuple
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, QFrame,
                               QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout, QVBoxLayout, QScrollArea, QStackedWidget)

from presentation.ui.viewmodels import StudentViewModel, GradeViewModel, ScheduleViewModel
from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.widgets import CircularImageWidget, get_initials
from domain.entities.user import UserRole
from domain.services.profile_image_service import ProfileImageService


class StudentDashboardBuilder(Builder):
    """
    Builder for the student dashboard view that shows grades, schedule and notifications
    """

    def __init__(
            self,
            wf: WidgetFactory,
            lf: LayoutFactory,
            student_name: str,
            on_logout: Callable[[], None] = None,
            on_navigate: Callable[[str], None] = None,
            grade_viewmodel: Optional[GradeViewModel] = None,
            schedule_viewmodel: Optional[ScheduleViewModel] = None,
            student_viewmodel: Optional[StudentViewModel] = None
    ):
        """
        Initialize the student dashboard builder

        :param wf: Widget factory
        :param lf: Layout factory
        :param student_name: Student name to display
        :param on_logout: Callback for logout action
        :param on_navigate: Callback for navigation
        :param grade_viewmodel: ViewModel for grades
        :param schedule_viewmodel: ViewModel for schedule
        :param student_viewmodel: ViewModel for student
        """
        self._wf = wf
        self._lf = lf
        self._student_name = student_name
        self._on_logout = on_logout or (lambda: None)
        self._on_navigate = on_navigate or (lambda section: None)
        self._grade_viewmodel = grade_viewmodel
        self._schedule_viewmodel = schedule_viewmodel
        self._student_viewmodel = student_viewmodel

        # Profile image service to handle profile images
        self._profile_image_service = ProfileImageService()

        # Current view/section
        self._current_section = "calificaciones"

        # Logger for this class
        self._logger = logging.getLogger(__name__)
        
        # Connect to viewmodel signals if available
        if self._grade_viewmodel:
            self._grade_viewmodel.gradesLoaded.connect(self._on_grades_loaded)
            # Trigger initial data load
            QTimer.singleShot(100, self._grade_viewmodel.load_grades)
            
        if self._schedule_viewmodel:
            self._schedule_viewmodel.scheduleLoaded.connect(self._on_schedule_loaded)
            # Trigger initial data load
            QTimer.singleShot(200, self._schedule_viewmodel.load_schedule)

        # Create container widget
        self._container = QWidget()
        self._container.setObjectName("student-dashboard-container")

        # Main layout
        self._main_layout = QGridLayout()
        self._container.setLayout(self._main_layout)

        # Create components
        self._create_left_navigation()
        self._create_welcome_banner()
        self._create_grades_section()
        self._create_schedule_section()
        self._create_notifications_section()
        self._create_user_info()

        # Assemble components
        self._assemble_layout()

        # Apply styles
        self._apply_styles()
        
    def _create_left_navigation(self) -> None:
        """Create left navigation panel"""
        self._nav_panel = QFrame()
        self._nav_panel.setObjectName("nav-panel")
        self._nav_panel.setFixedWidth(120)

        nav_layout = QVBoxLayout()
        self._nav_panel.setLayout(nav_layout)

        # App logo
        self._logo = QLabel("Uamitos - CA")
        self._logo.setObjectName("app-logo")
        nav_layout.addWidget(self._logo)

        # Navigation items
        nav_items = [
            ("Inicio", "inicio"),
            ("Calificaciones", "calificaciones"),
            ("Horario", "horario"),
            ("Notificaciones", "notificaciones"),
            ("Configuración", "configuracion")
        ]

        self._nav_buttons = {}
        for label, item_id in nav_items:
            btn = QPushButton(label)
            btn.setObjectName(f"nav-{item_id}")
            btn.setCheckable(True)

            # Set calificaciones as active by default
            if item_id == "calificaciones":
                btn.setChecked(True)
                
            # Ensure button text is visible
            btn.setStyleSheet("color: white; font-weight: bold;")

            # Connect navigation button to handler
            btn.clicked.connect(lambda checked, section=item_id: self._handle_navigation(section))

            nav_layout.addWidget(btn)
            self._nav_buttons[item_id] = btn

        # Add spacer
        nav_layout.addStretch(1)
        
    def _create_welcome_banner(self) -> None:
        """Create welcome banner section"""
        self._welcome_banner = QFrame()
        self._welcome_banner.setObjectName("welcome-container")
        
        welcome_layout = QHBoxLayout()
        self._welcome_banner.setLayout(welcome_layout)
        
        # Welcome message
        welcome_text_container = QVBoxLayout()
        
        welcome_message = QLabel(f"¡Bienvenido, {self._student_name}!")
        welcome_message.setObjectName("welcome-message")
        
        welcome_description = QLabel("Consulta tus calificaciones, horario de clases y notificaciones")
        welcome_description.setObjectName("welcome-description")
        
        welcome_text_container.addWidget(welcome_message)
        welcome_text_container.addWidget(welcome_description)
        welcome_text_container.addStretch(1)
        
        # Action button
        action_button = QPushButton("Ver calificaciones")
        action_button.setObjectName("action-button")
        action_button.clicked.connect(lambda: self._handle_navigation("calificaciones"))
        welcome_text_container.addWidget(action_button)
        
        # Student image
        student_image = QLabel("👨‍🎓")
        student_image.setObjectName("student-image")
        student_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addLayout(welcome_text_container, 2)
        welcome_layout.addWidget(student_image, 1)
        
    def _create_grades_section(self) -> None:
        """Create grades section with table"""
        # Section container
        self._grades_section = QFrame()
        self._grades_section.setObjectName("grades-section")

        grades_layout = QVBoxLayout()
        self._grades_section.setLayout(grades_layout)

        # Header with title
        header_layout = QHBoxLayout()

        self._grades_title = QLabel("Calificaciones")
        self._grades_title.setObjectName("section-title")
        
        header_layout.addWidget(self._grades_title)
        header_layout.addStretch(1)

        grades_layout.addLayout(header_layout)

        # Create grades table
        self._grades_table = QTableWidget()
        self._grades_table.setObjectName("grades-table")
        self._grades_table.setColumnCount(3)
        self._grades_table.setHorizontalHeaderLabels(["Materia", "Calificación", "Estado"])
        
        # Set header text color directly
        header_view = self._grades_table.horizontalHeader()
        header_view.setStyleSheet("QHeaderView::section { color: white; font-weight: bold; }")

        # Configure table appearance
        self._grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._grades_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._grades_table.setAlternatingRowColors(True)
        self._grades_table.setShowGrid(True)
        self._grades_table.setGridStyle(Qt.PenStyle.SolidLine)
        self._grades_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Get grades data from API (via view model)
        grade_data = self._get_grade_data()

        self._grades_table.setRowCount(len(grade_data))

        for row, (subject, grade, status) in enumerate(grade_data):
            self._grades_table.setItem(row, 0, QTableWidgetItem(subject))
            self._grades_table.setItem(row, 1, QTableWidgetItem(grade))
            
            status_item = QTableWidgetItem(status)
            if status == "Aprobado":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif status == "Reprobado":
                status_item.setForeground(Qt.GlobalColor.darkRed)
            else:
                status_item.setForeground(Qt.GlobalColor.darkYellow)
                
            self._grades_table.setItem(row, 2, status_item)

        grades_layout.addWidget(self._grades_table)
        
        # Add overall GPA section
        gpa_container = QFrame()
        gpa_layout = QHBoxLayout()
        gpa_container.setLayout(gpa_layout)
        
        gpa_label = QLabel("Promedio general:")
        gpa_label.setStyleSheet("font-weight: bold; color: #000000;")
        
        gpa_value = QLabel("8.7")  # This would come from the viewmodel
        gpa_value.setStyleSheet("font-weight: bold; color: #3a7bd5; font-size: 16px;")
        
        gpa_layout.addWidget(gpa_label)
        gpa_layout.addWidget(gpa_value)
        gpa_layout.addStretch(1)
        
        grades_layout.addWidget(gpa_container)
        
    def _create_schedule_section(self) -> None:
        """Create schedule section with timetable"""
        # Section container
        self._schedule_section = QFrame()
        self._schedule_section.setObjectName("schedule-section")

        schedule_layout = QVBoxLayout()
        self._schedule_section.setLayout(schedule_layout)

        # Header with title
        header_layout = QHBoxLayout()

        self._schedule_title = QLabel("Horario")
        self._schedule_title.setObjectName("section-title")

        header_layout.addWidget(self._schedule_title)
        header_layout.addStretch(1)

        schedule_layout.addLayout(header_layout)
        
        # Days of week headers
        days_container = QFrame()
        days_layout = QHBoxLayout()
        days_container.setLayout(days_layout)
        
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for day in days:
            day_label = QLabel(day)
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setStyleSheet("font-weight: bold; color: #000000;")
            days_layout.addWidget(day_label)
            
        schedule_layout.addWidget(days_container)
        
        # Schedule grid - simplified version
        schedule_grid = QGridLayout()
        
        # Time slots
        times = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]
        
        # Sample schedule data (would come from viewmodel)
        schedule_data = {
            (0, 0): {"subject": "Matemáticas", "room": "A101"},
            (0, 2): {"subject": "Física", "room": "B201"},
            (0, 4): {"subject": "Inglés", "room": "C301"},
            (1, 1): {"subject": "Historia", "room": "A102"},
            (1, 3): {"subject": "Química", "room": "B202"},
            (2, 0): {"subject": "Literatura", "room": "A103"},
            (2, 2): {"subject": "Biología", "room": "B203"},
            (3, 1): {"subject": "Computación", "room": "C302"},
            (3, 4): {"subject": "Arte", "room": "A104"},
            (4, 2): {"subject": "Educación Física", "room": "Gimnasio"},
        }
        
        for row, time in enumerate(times):
            # Add time label
            time_label = QLabel(time)
            time_label.setStyleSheet("color: #000000; font-weight: bold;")
            schedule_grid.addWidget(time_label, row + 1, 0)
            
            # Add classes
            for col in range(5):  # 5 days
                cell = QFrame()
                cell.setObjectName("schedule-cell")
                cell.setStyleSheet("background-color: white; border: 1px solid #e0e0e0; border-radius: 5px;")
                cell_layout = QVBoxLayout()
                cell.setLayout(cell_layout)
                
                if (row, col) in schedule_data:
                    class_data = schedule_data[(row, col)]
                    subject = QLabel(class_data["subject"])
                    subject.setStyleSheet("color: #000000; font-weight: bold;")
                    room = QLabel(class_data["room"])
                    room.setStyleSheet("color: #333333;")
                    
                    cell_layout.addWidget(subject)
                    cell_layout.addWidget(room)
                    
                    # Set class color based on subject
                    cell.setStyleSheet("background-color: rgba(58, 123, 213, 0.1); border: 1px solid #3a7bd5; border-radius: 5px;")
                
                schedule_grid.addWidget(cell, row + 1, col + 1)
                
        schedule_layout.addLayout(schedule_grid)
        
    def _create_notifications_section(self) -> None:
        """Create notifications section"""
        # Section container
        self._notifications_section = QFrame()
        self._notifications_section.setObjectName("notifications-section")

        notifications_layout = QVBoxLayout()
        self._notifications_section.setLayout(notifications_layout)

        # Header with title
        header_layout = QHBoxLayout()

        self._notifications_title = QLabel("Notificaciones")
        self._notifications_title.setObjectName("section-title")

        header_layout.addWidget(self._notifications_title)
        header_layout.addStretch(1)

        notifications_layout.addLayout(header_layout)
        
        # Create notification items
        notifications = [
            {"title": "Nuevo trabajo asignado", "subject": "Matemáticas", "date": "Hoy", "priority": "high"},
            {"title": "Calificación publicada", "subject": "Física", "date": "Ayer", "priority": "medium"},
            {"title": "Recordatorio de entrega", "subject": "Historia", "date": "2 días", "priority": "high"},
            {"title": "Cambio de horario", "subject": "Inglés", "date": "3 días", "priority": "low"},
        ]
        
        for notification in notifications:
            self._create_notification_item(notification, notifications_layout)
            
    def _create_notification_item(self, notification: dict, parent_layout: QVBoxLayout) -> None:
        """Create a notification item"""
        # Notification container
        notification_item = QFrame()
        notification_item.setObjectName(f"notification-{notification['priority']}")
        
        item_layout = QHBoxLayout()
        notification_item.setLayout(item_layout)
        
        # Icon based on priority
        icon_map = {
            "high": "🔴",
            "medium": "🟠",
            "low": "🟢"
        }
        
        icon = QLabel(icon_map.get(notification["priority"], "⚪"))
        icon.setObjectName("notification-icon")
        icon.setStyleSheet("color: #000000; font-size: 16px;")
        
        # Notification content
        content_layout = QVBoxLayout()
        
        title = QLabel(notification["title"])
        title.setObjectName("notification-title")
        title.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        
        subject = QLabel(f"Materia: {notification['subject']}")
        subject.setObjectName("notification-subject")
        subject.setStyleSheet("color: #333333;")
        
        content_layout.addWidget(title)
        content_layout.addWidget(subject)
        
        # Date
        date = QLabel(notification["date"])
        date.setObjectName("notification-date")
        date.setStyleSheet("color: #777777;")
        
        # Assemble layout
        item_layout.addWidget(icon)
        item_layout.addLayout(content_layout, 1)
        item_layout.addWidget(date)
        
        parent_layout.addWidget(notification_item)

    def _create_user_info(self) -> None:
        """Create user info section in header"""
        self._user_info = QFrame()
        self._user_info.setObjectName("user-info")

        info_layout = QHBoxLayout()
        self._user_info.setLayout(info_layout)

        # Get user initials for placeholder
        initials = get_initials(self._student_name)

        # Create circular profile image
        self._profile_image = CircularImageWidget(
            size=40,
            placeholder_bg_color="#5a7a95",
            placeholder_text=initials
        )
        self._profile_image.setObjectName("profile-image")

        # Try to load profile image if available
        student_id = self._student_name.lower().replace(" ", "_")
        image_path = self._profile_image_service.get_image_path(student_id, "student")
        self._profile_image.setImage(image_path)

        # User name
        user_name = QLabel(f"Nombre de Usuario: {self._student_name}")
        user_name.setObjectName("user-name")
        user_name.setStyleSheet("color: #000000; font-weight: bold;")

        # Logout button
        self._logout_button = QPushButton("Cerrar sesión")
        self._logout_button.setObjectName("logout-button")
        self._logout_button.clicked.connect(self._on_logout)

        info_layout.addWidget(self._profile_image)
        info_layout.addWidget(user_name, 1)  # Give name more stretch
        info_layout.addWidget(self._logout_button)

    def _assemble_layout(self) -> None:
        """Assemble all components into main layout"""
        # First row: user info
        self._main_layout.addWidget(self._user_info, 0, 1, 1, 3)

        # Left navigation panel (spans all rows)
        self._main_layout.addWidget(self._nav_panel, 0, 0, 6, 1)

        # Second row: welcome banner
        self._main_layout.addWidget(self._welcome_banner, 1, 1, 1, 3)

        # Third row: grades section
        self._main_layout.addWidget(self._grades_section, 2, 1, 2, 3)

        # Fourth row: schedule section
        self._main_layout.addWidget(self._schedule_section, 4, 1, 1, 2)
        
        # Fourth row, right column: notifications section
        self._main_layout.addWidget(self._notifications_section, 4, 3, 1, 1)

        # Set column and row stretches
        self._main_layout.setColumnStretch(0, 0)  # Navigation doesn't stretch
        self._main_layout.setColumnStretch(1, 1)
        self._main_layout.setColumnStretch(2, 1)
        self._main_layout.setColumnStretch(3, 1)

        self._main_layout.setRowStretch(0, 0)  # Header row doesn't stretch
        self._main_layout.setRowStretch(1, 0)  # Welcome banner doesn't stretch
        self._main_layout.setRowStretch(2, 2)  # Grades stretches more
        self._main_layout.setRowStretch(3, 0)  
        self._main_layout.setRowStretch(4, 1)  # Schedule and notifications stretch less

    def _apply_styles(self) -> None:
        """Apply styles to the dashboard"""
        # Main styles
        self._container.setStyleSheet("""
                #student-dashboard-container {
                    background-color: #f8f9fa;
                }

                /* Navigation panel */
                #nav-panel {
                    background-color: #3a7bd5;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 6px;
                }

                #app-logo {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    padding: 10px 0;
                    font-family: "Segoe UI", Arial, sans-serif;
                    letter-spacing: 0.5px;
                }

                #nav-panel QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: left;
                    font-size: 15px;
                    font-weight: 500;
                    font-family: "Segoe UI", Arial, sans-serif;
                }

                #nav-panel QPushButton:checked {
                    background-color: rgba(255, 255, 255, 0.2);
                    color: white;
                    border-radius: 4px;
                }

                /* Welcome banner */
                #welcome-container {
                    background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);
                    color: white;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }

                #welcome-message {
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
                    font-family: "Segoe UI", Arial, sans-serif;
                }

                #welcome-description {
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 16px;
                    margin-bottom: 20px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    font-weight: 500;
                }
                
                #student-image {
                    font-size: 70px;
                    color: white;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }
                
                #action-button {
                    background-color: white;
                    color: #3a7bd5;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 18px;
                    font-weight: bold;
                    font-size: 15px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    transition: all 0.3s;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }

                #action-button:hover {
                    background-color: rgba(255, 255, 255, 0.9);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
                }
                
                /* Sections */
                #grades-section, #schedule-section, #notifications-section {
                    background-color: white;
                    border-radius: 8px;
                    padding: 15px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    border: 1px solid #e0e0e0;
                }
                
                #section-title {
                    font-size: 22px;
                    font-weight: bold;
                    color: #3a7bd5;
                    margin-bottom: 15px;
                    font-family: "Segoe UI", Arial, sans-serif;
                }

                /* Grades table */
                #grades-table {
                    border: none;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    color: #000000;
                }

                #grades-table::item {
                    padding: 8px;
                    font-size: 14px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    color: #000000;
                }

                #grades-table::item:selected {
                    background-color: #4facfe;
                    color: white;
                }
                
                /* Notifications */
                #notification-high, #notification-medium, #notification-low {
                    background-color: white;
                    border-radius: 6px;
                    padding: 10px;
                    margin-bottom: 8px;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                }
                
                #notification-high {
                    border-left: 4px solid #e53935;
                }
                
                #notification-medium {
                    border-left: 4px solid #fb8c00;
                }
                
                #notification-low {
                    border-left: 4px solid #43a047;
                }
                
                /* User info */
                #user-info {
                    padding: 10px;
                    margin-bottom: 10px;
                }
                
                #logout-button {
                    background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
                    color: white;
                    font-weight: bold;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: all 0.2s ease;
                }
                
                #logout-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
                }
            """)

    def _get_grade_data(self) -> List[Tuple[str, str, str]]:
        """Get grade data for displaying in the table
        
        :return: List of (subject, grade, status) tuples
        """
        # Try to get data from the viewmodel if available
        if self._grade_viewmodel:
            try:
                # Trigger data loading if not already loaded
                self._grade_viewmodel.load_grades()
                
                # Return empty list for now as data will come through the signal
                return []
            except Exception as e:
                self._logger.error(f"Error loading grades from viewmodel: {e}")
                
        # Fallback to dummy data if viewmodel is not available or failed
        return [
            ("Matemáticas", "9.5", "Aprobado"),
            ("Historia", "8.7", "Aprobado"),
            ("Física", "7.8", "Aprobado"),
            ("Química", "9.0", "Aprobado"),
            ("Literatura", "5.9", "Reprobado"),
            ("Educación Física", "8.5", "Aprobado"),
            ("Inglés", "6.5", "En curso")
        ]
        
    def _on_grades_loaded(self, grades) -> None:
        """Handle grades loaded signal from grade viewmodel
        
        :param grades: List of loaded grades
        """
        self._logger.info(f"Grades loaded: {len(grades) if grades else 0}")
        
        # Update the UI with the loaded grades
        if hasattr(self, '_grades_table') and self._grades_table:
            # Clear existing rows
            self._grades_table.setRowCount(0)
            
            if grades:
                # Add new rows for each grade
                self._grades_table.setRowCount(len(grades))
                
                for row, grade in enumerate(grades):
                    # Extract subject, grade and status
                    subject = grade.get('subject_name', 'N/A')
                    grade_value = str(grade.get('grade', 'N/A'))
                    
                    # Determine status based on grade value
                    status = "En curso"
                    if grade.get('is_final', False):
                        if float(grade_value) >= 6.0:
                            status = "Aprobado"
                        else:
                            status = "Reprobado"
                    
                    self._grades_table.setItem(row, 0, QTableWidgetItem(subject))
                    self._grades_table.setItem(row, 1, QTableWidgetItem(grade_value))
                    
                    status_item = QTableWidgetItem(status)
                    if status == "Aprobado":
                        status_item.setForeground(Qt.GlobalColor.darkGreen)
                    elif status == "Reprobado":
                        status_item.setForeground(Qt.GlobalColor.darkRed)
                    else:
                        status_item.setForeground(Qt.GlobalColor.darkYellow)
                        
                    self._grades_table.setItem(row, 2, status_item)
                    
    def _on_schedule_loaded(self, schedule) -> None:
        """Handle schedule loaded signal from schedule viewmodel
        
        :param schedule: Dictionary of schedule data
        """
        self._logger.info(f"Schedule loaded: {len(schedule) if schedule else 0} items")
        # Would update the schedule UI based on loaded data
                
    def _handle_navigation(self, section: str) -> None:
        """Handle navigation between sections
        
        :param section: Section to navigate to
        """
        if section == self._current_section:
            return
            
        # Update current section
        self._current_section = section
        
        # Update UI to reflect the new section
        for btn_id, btn in self._nav_buttons.items():
            btn.setChecked(btn_id == section)
            
        # Update content visibility based on selected section
        if section == "calificaciones":
            if hasattr(self, '_grades_section'):
                self._grades_section.setVisible(True)
            if hasattr(self, '_schedule_section'):
                self._schedule_section.setVisible(False)
            if hasattr(self, '_notifications_section'):
                self._notifications_section.setVisible(False)
        elif section == "horario":
            if hasattr(self, '_grades_section'):
                self._grades_section.setVisible(False)
            if hasattr(self, '_schedule_section'):
                self._schedule_section.setVisible(True)
            if hasattr(self, '_notifications_section'):
                self._notifications_section.setVisible(False)
        elif section == "notificaciones":
            if hasattr(self, '_grades_section'):
                self._grades_section.setVisible(False)
            if hasattr(self, '_schedule_section'):
                self._schedule_section.setVisible(False)
            if hasattr(self, '_notifications_section'):
                self._notifications_section.setVisible(True)
                
        # Trigger data loading based on the selected section
        if section == "calificaciones" and self._grade_viewmodel:
            self._grade_viewmodel.load_grades()
        elif section == "horario" and self._schedule_viewmodel:
            self._schedule_viewmodel.load_schedule()
            
        # Call external navigation handler if provided
        self._on_navigate(section)
        
        # Log navigation
        self._logger.info(f"Navigated to section: {section}")
        
    def build(self) -> QWidget:
        """
        Build and return the final dashboard widget
        
        :return: The constructed dashboard widget
        """
        return self._container
        
    def set_on_logout(self, callback: Callable[[], None]) -> None:
        """
        Set or update the logout callback
        
        :param callback: Function to call on logout
        """
        self._on_logout = callback
        if hasattr(self, '_logout_button'):
            self._logout_button.clicked.disconnect()
            self._logout_button.clicked.connect(callback)
            
    def create(self):
        """Create a new instance of this builder"""
        return type(self)(
            self._wf,
            self._lf,
            self._student_name,
            self._on_logout,
            self._on_navigate,
            self._grade_viewmodel,
            self._schedule_viewmodel,
            self._student_viewmodel
        )

    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)