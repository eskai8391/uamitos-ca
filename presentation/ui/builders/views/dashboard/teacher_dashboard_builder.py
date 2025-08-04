import logging
from typing import Callable, Dict, Optional, List, Tuple
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, QFrame,
                               QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout, QVBoxLayout, QScrollArea, QStackedWidget)

from presentation.ui.viewmodels import StudentViewModel, TeacherViewModel, EventViewModel

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.widgets import CircularImageWidget, get_initials
from domain.entities.user import UserRole
from domain.services.profile_image_service import ProfileImageService


class TeacherDashboardBuilder(Builder):
    """
    Builder for the teacher dashboard view that shows student list, attendance and calendar
    """

    def __init__(
            self,
            wf: WidgetFactory,
            lf: LayoutFactory,
            teacher_name: str,
            on_logout: Callable[[], None] = None,
            on_navigate: Callable[[str], None] = None,
            student_viewmodel: Optional[StudentViewModel] = None,
            teacher_viewmodel: Optional[TeacherViewModel] = None,
            event_viewmodel: Optional[EventViewModel] = None
    ):
        """
        Initialize the teacher dashboard builder

        :param wf: Widget factory
        :param lf: Layout factory
        :param teacher_name: Teacher name to display
        :param on_logout: Callback for logout action
        """
        self._wf = wf
        self._lf = lf
        self._teacher_name = teacher_name
        self._on_logout = on_logout or (lambda: None)
        self._on_navigate = on_navigate or (lambda section: None)
        self._student_viewmodel = student_viewmodel
        self._teacher_viewmodel = teacher_viewmodel
        self._event_viewmodel = event_viewmodel

        # Profile image service to handle profile images
        self._profile_image_service = ProfileImageService()

        # Current view/section
        self._current_section = "estudiantes"

        # Logger for this class
        self._logger = logging.getLogger(__name__)
        
        # Connect to viewmodel signals if available
        if self._student_viewmodel:
            self._student_viewmodel.studentsLoaded.connect(self._on_students_loaded)
            # Trigger initial data load
            QTimer.singleShot(100, self._student_viewmodel.load_students)

        if self._teacher_viewmodel:
            self._teacher_viewmodel.teachersLoaded.connect(self._on_teachers_loaded)
            # Trigger initial data load
            QTimer.singleShot(200, self._teacher_viewmodel.load_teachers)

        if self._event_viewmodel:
            self._event_viewmodel.upcomingEventsLoaded.connect(self._on_events_loaded)
            self._event_viewmodel.monthlyAttendanceLoaded.connect(self._on_monthly_attendance_loaded)
            # Trigger initial data loads
            QTimer.singleShot(300, self._event_viewmodel.load_upcoming_events)
            QTimer.singleShot(400, self._event_viewmodel.load_monthly_attendance)

        # Create container widget
        self._container = QWidget()
        self._container.setObjectName("teacher-dashboard-container")

        # Main layout
        self._main_layout = QGridLayout()
        self._container.setLayout(self._main_layout)

        # Create components
        self._create_left_navigation()
        self._create_search_bar()
        self._create_control_cards()
        self._create_students_section()
        self._create_events_section()
        self._create_attendance_chart()
        self._create_teachers_list()
        self._create_user_info()

        # Assemble components
        self._assemble_layout()

        # Apply styles
        self._apply_styles()

    def _create_left_navigation(self) -> None:
        """Create left navigation panel"""
        self._nav_panel = QFrame()
        self._nav_panel.setObjectName("nav-panel")
        self._nav_panel.setFixedWidth(160)

        nav_layout = QVBoxLayout()
        self._nav_panel.setLayout(nav_layout)

        # App logo
        self._logo = QLabel("Uamitos - CA")
        self._logo.setObjectName("app-logo")
        nav_layout.addWidget(self._logo)

        # Navigation items
        nav_items = [
            ("Inicio", "inicio"),
            ("Estudiantes", "estudiantes"),
            ("Profesores", "profesores"),
            ("Eventos", "eventos")
        ]

        self._nav_buttons = {}
        for label, item_id in nav_items:
            btn = QPushButton(label)
            btn.setObjectName(f"nav-{item_id}")
            btn.setCheckable(True)

            # Set estudiantes as active by default
            if item_id == "estudiantes":
                btn.setChecked(True)
                
            # Ensure button text is visible
            btn.setStyleSheet("color: white; font-weight: bold;")

            # Connect navigation button to handler
            btn.clicked.connect(lambda checked, section=item_id: self._handle_navigation(section))

            nav_layout.addWidget(btn)
            self._nav_buttons[item_id] = btn

        # Add spacer
        nav_layout.addStretch(1)

    def _create_search_bar(self) -> None:
        """Create search bar"""
        self._search_bar = QLineEdit()
        self._search_bar.setObjectName("search-bar")
        self._search_bar.setPlaceholderText("Buscar estudiantes...")
        self._search_bar.returnPressed.connect(self._handle_search)

    def _create_control_cards(self) -> None:
        """Create control cards section"""
        self._control_cards_container = QFrame()
        self._control_cards_container.setObjectName("control-cards")

        cards_layout = QHBoxLayout()
        self._control_cards_container.setLayout(cards_layout)

        # Create cards with click handlers
        self._create_control_card("Control\nEstudiantes", "students-card", cards_layout,
                                  lambda: self._handle_navigation("estudiantes"))
        self._create_control_card("Control\nAdministrativos", "admin-card", cards_layout,
                                  lambda: self._handle_navigation("profesores"))
        self._create_control_card("Control\nHorarios", "schedule-card", cards_layout,
                                  lambda: self._handle_navigation("eventos"))

    def _create_control_card(self, title: str, obj_name: str, parent_layout: QHBoxLayout,
                             on_click: Callable[[], None] = None) -> None:
        """Create a control card with arrow indicator"""
        card = QFrame()
        card.setObjectName(obj_name)

        # Make the card clickable
        if on_click:
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            # Create a proper subclass to handle mouse events
            orig_mouse_press = card.mousePressEvent

            def new_mouse_press(event):
                on_click()
                if orig_mouse_press:
                    orig_mouse_press(event)

            card.mousePressEvent = new_mouse_press

        card_layout = QHBoxLayout()
        card.setLayout(card_layout)

        # Title label
        title_label = QLabel(title)
        title_label.setObjectName(f"{obj_name}-title")

        # Arrow indicator
        arrow = QLabel("»")
        arrow.setObjectName(f"{obj_name}-arrow")

        # Add to card layout
        card_layout.addWidget(title_label)
        card_layout.addWidget(arrow, 0, Qt.AlignmentFlag.AlignRight)

        # Add card to parent layout
        parent_layout.addWidget(card)

    def _create_students_section(self) -> None:
        """Create students section with table"""
        # Section container
        self._students_section = QFrame()
        self._students_section.setObjectName("students-section")

        students_layout = QVBoxLayout()
        self._students_section.setLayout(students_layout)

        # Header with title and view all link
        header_layout = QHBoxLayout()

        self._students_title = QLabel("Estudiantes")
        self._students_title.setObjectName("section-title")

        self._view_all = QLabel("Ver todos")
        self._view_all.setObjectName("view-all-link")
        self._view_all.setCursor(Qt.CursorShape.PointingHandCursor)
        # Create a proper subclass to handle mouse events
        orig_mouse_press = self._view_all.mousePressEvent

        def new_mouse_press(event):
            self._handle_view_all_students()
            if orig_mouse_press:
                orig_mouse_press(event)

        self._view_all.mousePressEvent = new_mouse_press

        header_layout.addWidget(self._students_title)
        header_layout.addStretch(1)
        header_layout.addWidget(self._view_all)

        students_layout.addLayout(header_layout)

        # Create student table
        self._students_table = QTableWidget()
        self._students_table.setObjectName("students-table")
        self._students_table.setColumnCount(3)
        self._students_table.setHorizontalHeaderLabels(["Nombre", "Grado", "Asistencia"])
        
        # Set header text color directly
        header_view = self._students_table.horizontalHeader()
        header_view.setStyleSheet("QHeaderView::section { color: white; font-weight: bold; }")

        # Configure table appearance
        self._students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._students_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._students_table.setAlternatingRowColors(True)
        self._students_table.setShowGrid(True)
        self._students_table.setGridStyle(Qt.PenStyle.SolidLine)
        self._students_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._students_table.cellDoubleClicked.connect(self._handle_student_selected)

        # Get student data from API (via view model)
        student_data = self._get_student_data()

        self._students_table.setRowCount(len(student_data))

        for row, (name, grade, attendance) in enumerate(student_data):
            self._students_table.setItem(row, 0, QTableWidgetItem(name))
            self._students_table.setItem(row, 1, QTableWidgetItem(grade))
            self._students_table.setItem(row, 2, QTableWidgetItem(attendance))

        students_layout.addWidget(self._students_table)

    def _create_events_section(self) -> None:
        """Create events calendar section"""
        # Main container
        self._events_section = QFrame()
        self._events_section.setObjectName("events-section")

        events_layout = QVBoxLayout()
        self._events_section.setLayout(events_layout)

        # Header with events title
        header_layout = QHBoxLayout()

        events_icon = QLabel("📅")
        events_icon.setObjectName("events-icon")

        events_title = QLabel("Eventos")
        events_title.setObjectName("events-title")

        header_layout.addWidget(events_icon)
        header_layout.addWidget(events_title)
        header_layout.addStretch(1)

        events_layout.addLayout(header_layout)

        # Load events from API via viewmodel
        if self._event_viewmodel:
            self._event_viewmodel.load_upcoming_events(7)  # Load events for the next 7 days
        else:
            # Fallback to dummy data if no viewmodel available
            self._create_event_card("Lunes", "28", "Clase especial de matemáticas", "09:00 AM - 10:00 AM", "En 1 días",
                                    events_layout)
            self._create_event_card("Martes", "29", "Webinar de orientación", "01:00 PM - 02:30 PM", "En 2 días",
                                    events_layout)
            self._create_event_card("Viernes", "1", "Excursión", "Todo el día", "En 5 días", events_layout)

    def _create_event_card(self, day: str, date: str, title: str, time: str, days_left: str,
                           parent_layout: QVBoxLayout) -> None:
        """Create an event card"""
        # Card container
        card = QFrame()
        card.setObjectName("event-card")
        card.setStyleSheet("""
            #event-card {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin: 5px 0;
            }
        """)

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(10, 10, 10, 10)  # Add padding inside card
        card.setLayout(card_layout)

        # Left side with date
        date_container = QFrame()
        date_container.setObjectName("event-date")
        date_container.setFixedWidth(70)  # Slightly wider for better alignment
        date_container.setStyleSheet("""
            #event-date {
                background-color: #3a7bd5;
                color: white;
                border-radius: 6px;
                padding: 3px;
            }
        """)

        date_layout = QVBoxLayout()
        date_layout.setContentsMargins(5, 8, 5, 8)  # More vertical space
        date_container.setLayout(date_layout)

        day_label = QLabel(day)
        day_label.setObjectName("event-day")
        day_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_number = QLabel(date)
        date_number.setObjectName("event-date-number")
        date_number.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        date_number.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_month = QLabel("Jul.")
        date_month.setObjectName("event-month")
        date_month.setStyleSheet("color: white; font-size: 12px;")
        date_month.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_layout.addWidget(day_label)
        date_layout.addWidget(date_number)
        date_layout.addWidget(date_month)

        # Right side with event details
        details_container = QFrame()
        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(10, 2, 2, 2)  # Add left padding for spacing
        details_container.setLayout(details_layout)

        event_title = QLabel(title)
        event_title.setObjectName("event-title")
        event_title.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        # Make sure title wraps properly
        event_title.setWordWrap(True)

        event_time = QLabel(f"🕓 {time}")
        event_time.setObjectName("event-time")
        event_time.setStyleSheet("color: #000000; font-weight: 500; font-size: 12px;")

        details_layout.addWidget(event_title)
        details_layout.addWidget(event_time)
        details_layout.addStretch(1)  # Push content to the top

        # Days left label on the right
        days_left_label = QLabel(days_left)
        days_left_label.setObjectName("days-left")
        days_left_label.setStyleSheet("""
            color: #ffffff; 
            font-weight: bold; 
            font-size: 12px;
            background-color: #4CAF50;
            border-radius: 10px;
            padding: 3px 8px;
        """)
        days_left_label.setFixedHeight(24)  # Fixed height for better alignment

        # Assemble card
        card_layout.addWidget(date_container)
        card_layout.addWidget(details_container, 1)
        card_layout.addWidget(days_left_label)

        # Add to parent layout
        parent_layout.addWidget(card)

    def _create_attendance_chart(self) -> None:
        """Create monthly attendance chart"""
        # Container
        self._attendance_section = QFrame()
        self._attendance_section.setObjectName("attendance-section")

        attendance_layout = QVBoxLayout()
        self._attendance_section.setLayout(attendance_layout)

        # Header with title and view all link
        header_layout = QHBoxLayout()

        chart_title = QLabel("Asistencia Mensual")
        chart_title.setObjectName("section-title")

        view_more = QLabel("Ver más")
        view_more.setObjectName("view-all-link")
        view_more.setCursor(Qt.CursorShape.PointingHandCursor)
        # Create a proper subclass to handle mouse events
        orig_mouse_press = view_more.mousePressEvent

        def new_mouse_press(event):
            self._handle_view_all_attendance()
            if orig_mouse_press:
                orig_mouse_press(event)

        view_more.mousePressEvent = new_mouse_press

        header_layout.addWidget(chart_title)
        header_layout.addStretch(1)
        header_layout.addWidget(view_more)

        attendance_layout.addLayout(header_layout)

        # Chart container
        chart_frame = QFrame()
        chart_frame.setObjectName("chart-container")
        chart_layout = QHBoxLayout()
        chart_frame.setLayout(chart_layout)
        
        # Store the chart layout for later updates
        self._chart_layout = chart_layout

        # Set a minimum height for the chart container to ensure it displays properly
        chart_frame.setMinimumHeight(240)
        chart_frame.setStyleSheet("""
            #chart-container {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # Add a chart title inside the container
        chart_title_container = QWidget()
        chart_title_layout = QHBoxLayout(chart_title_container)
        chart_title_layout.setContentsMargins(5, 0, 5, 0)
        
        attendance_chart_title = QLabel("Porcentaje de Asistencia")
        attendance_chart_title.setStyleSheet("color: #555; font-size: 14px; font-weight: bold;")
        
        chart_title_layout.addWidget(attendance_chart_title)
        chart_title_layout.addStretch(1)
        
        attendance_layout.addWidget(chart_title_container)
        
        # Load monthly attendance data from API via viewmodel
        if self._event_viewmodel:
            self._event_viewmodel.load_monthly_attendance(5)  # Load data for 5 months
            # We'll update the chart when the data is loaded via the signal
            # The bars will be created in the _on_monthly_attendance_loaded method
        else:
            # Fallback to dummy data if no viewmodel available
            months = ["Ene", "Feb", "Mar", "Abr", "May"]
            values = [70, 80, 75, 85, 90]
            
            for month, value in zip(months, values):
                bar_container = QFrame()
                bar_container.setFixedWidth(60)
                bar_layout = QVBoxLayout()
                bar_container.setLayout(bar_layout)
                
                # Value label (percentage)
                value_label = QLabel(f"{value}%")
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 13px;")

                # Bar with gradient based on value
                bar = QFrame()
                bar.setObjectName("attendance-bar")
                bar.setFixedHeight(int(value * 1.8))  # Scale value to height
                
                # Apply color based on value
                if value >= 90:
                    color = "#4CAF50"  # Green for excellent
                elif value >= 80:
                    color = "#2196F3"  # Blue for good
                elif value >= 70:
                    color = "#FF9800"  # Orange for average
                else:
                    color = "#F44336"  # Red for poor
                    
                bar.setStyleSheet(f"""
                    #attendance-bar {{   
                        background-color: {color};
                        border-radius: 4px;
                    }}
                """)

                # Month label
                month_label = QLabel(month)
                month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                month_label.setStyleSheet("color: #000000; font-weight: bold;")

                # Add widgets to layout with proper spacing
                bar_layout.addWidget(value_label)
                bar_layout.addSpacing(5)
                bar_layout.addStretch(1)  # Push bar to bottom
                bar_layout.addWidget(bar)
                bar_layout.addSpacing(5)
                bar_layout.addWidget(month_label)

                chart_layout.addWidget(bar_container)

        # Legend
        legend_layout = QHBoxLayout()

        attendance_color = QFrame()
        attendance_color.setObjectName("attendance-color")
        attendance_color.setFixedSize(15, 15)

        attendance_label = QLabel("Asistencia")

        absence_color = QFrame()
        absence_color.setObjectName("absence-color")
        absence_color.setFixedSize(15, 15)

        absence_label = QLabel("Inasistencia")

        legend_layout.addWidget(attendance_color)
        legend_layout.addWidget(attendance_label)
        legend_layout.addSpacing(20)
        legend_layout.addWidget(absence_color)
        legend_layout.addWidget(absence_label)
        legend_layout.addStretch(1)

        attendance_layout.addWidget(chart_frame)
        attendance_layout.addLayout(legend_layout)

    def _create_teachers_list(self) -> None:
        """Create teachers list section"""
        # Container
        self._teachers_section = QFrame()
        self._teachers_section.setObjectName("teachers-section")

        teachers_layout = QVBoxLayout()
        self._teachers_section.setLayout(teachers_layout)

        # Header
        header_layout = QHBoxLayout()

        teachers_title = QLabel("Lista de profesores")
        teachers_title.setObjectName("section-title")

        view_more_teachers = QLabel("Ver más")
        view_more_teachers.setObjectName("view-all-link")
        view_more_teachers.setCursor(Qt.CursorShape.PointingHandCursor)
        # Create a proper subclass to handle mouse events
        orig_mouse_press = view_more_teachers.mousePressEvent

        def new_mouse_press(event):
            self._handle_view_all_teachers()
            if orig_mouse_press:
                orig_mouse_press(event)

        view_more_teachers.mousePressEvent = new_mouse_press

        header_layout.addWidget(teachers_title)
        header_layout.addStretch(1)
        header_layout.addWidget(view_more_teachers)

        teachers_layout.addLayout(header_layout)

        # Teachers list
        teachers_list_layout = QHBoxLayout()

        # Get teacher data from API
        teacher_data = self._get_teacher_data()

        for name, subject in teacher_data:
            # Teacher card
            teacher_card = QFrame()
            teacher_card.setObjectName("teacher-card")

            card_layout = QVBoxLayout()
            teacher_card.setLayout(card_layout)

            # Create circular profile image for teacher
            initials = get_initials(name)
            avatar = CircularImageWidget(size=60, placeholder_bg_color="#8ecaef", placeholder_text=initials)
            avatar.setObjectName("teacher-avatar")

            # Try to load teacher profile image
            teacher_id = name.lower().replace(" ", "_")
            image_path = self._profile_image_service.get_image_path(teacher_id, "teacher")
            avatar.setImage(image_path)

            # Name (clickable)
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setObjectName("teacher-name")
            name_label.setCursor(Qt.CursorShape.PointingHandCursor)
            # Create a proper subclass to handle mouse events with teacher parameter
            teacher_name = name  # Capture the current teacher name
            orig_mouse_press = name_label.mousePressEvent

            def new_mouse_press(event, t=teacher_name):
                self._handle_teacher_selected(t)
                if orig_mouse_press:
                    orig_mouse_press(event)

            name_label.mousePressEvent = new_mouse_press

            # Subject
            subject_label = QLabel(subject)
            subject_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subject_label.setObjectName("teacher-subject")

            card_layout.addWidget(avatar)
            card_layout.addWidget(name_label)
            card_layout.addWidget(subject_label)

            teachers_list_layout.addWidget(teacher_card)

        teachers_layout.addLayout(teachers_list_layout)

    def _create_user_info(self) -> None:
        """Create user info section in header"""
        self._user_info = QFrame()
        self._user_info.setObjectName("user-info")

        info_layout = QHBoxLayout()
        self._user_info.setLayout(info_layout)

        # Get user initials for placeholder
        initials = get_initials(self._teacher_name)

        # Create circular profile image
        self._profile_image = CircularImageWidget(
            size=40,
            placeholder_bg_color="#5a7a95",
            placeholder_text=initials
        )
        self._profile_image.setObjectName("profile-image")

        # Try to load profile image if available
        teacher_id = self._teacher_name.lower().replace(" ", "_")
        image_path = self._profile_image_service.get_image_path(teacher_id, "teacher")
        self._profile_image.setImage(image_path)

        # User name
        user_name = QLabel(f"Nombre de Usuario: {self._teacher_name}")
        user_name.setObjectName("user-name")

        # Logout button
        self._logout_button = QPushButton("Cerrar sesión")
        self._logout_button.setObjectName("logout-button")
        self._logout_button.clicked.connect(self._on_logout)

        info_layout.addWidget(self._profile_image)
        info_layout.addWidget(user_name, 1)  # Give name more stretch
        info_layout.addWidget(self._logout_button)

    def _assemble_layout(self) -> None:
        """Assemble all components into main layout"""
        # First row: search bar and user info
        self._main_layout.addWidget(self._search_bar, 0, 1, 1, 3)
        self._main_layout.addWidget(self._user_info, 0, 4, 1, 1)

        # Left navigation panel (spans all rows)
        self._main_layout.addWidget(self._nav_panel, 0, 0, 6, 1)
        
        # Create a stacked widget to hold different content pages
        self._content_stack = QStackedWidget()
        
        # Create page for "inicio" tab (welcome/home)
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        
        # Create welcome banner for home page
        welcome_frame = QFrame()
        welcome_frame.setObjectName("welcome-container")
        welcome_layout = QHBoxLayout(welcome_frame)
        
        # Welcome message in a vertical layout
        welcome_text_container = QVBoxLayout()
        
        welcome_message = QLabel(f"¡Bienvenido, {self._teacher_name}!")
        welcome_message.setObjectName("welcome-message")
        welcome_message.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        
        welcome_description = QLabel("Consulta el rendimiento y asistencia de tus estudiantes")
        welcome_description.setObjectName("welcome-description")
        welcome_description.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px;")
        
        # Action button
        action_button = QPushButton("Ver Estudiantes")
        action_button.setObjectName("action-button")
        action_button.clicked.connect(lambda: self._handle_navigation("estudiantes"))
        
        welcome_text_container.addWidget(welcome_message)
        welcome_text_container.addWidget(welcome_description)
        welcome_text_container.addStretch(1)
        welcome_text_container.addWidget(action_button)
        
        # Teacher image
        teacher_image = QLabel("👨‍🏫")
        teacher_image.setObjectName("teacher-image")
        teacher_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        teacher_image.setStyleSheet("font-size: 70px; color: white; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);")
        
        welcome_layout.addLayout(welcome_text_container, 2)
        welcome_layout.addWidget(teacher_image, 1)
        
        home_layout.addWidget(welcome_frame)
        
        # Create welcome info for home page
        info_frame = QFrame()
        info_frame.setObjectName("welcome-info-frame")
        info_layout = QVBoxLayout(info_frame)
        
        instructions_title = QLabel("Bienvenido a tu panel de docente")
        instructions_title.setObjectName("instructions-title")
        instructions_title.setStyleSheet("color: #3a7bd5; font-size: 18px; font-weight: bold;")
        info_layout.addWidget(instructions_title)
        
        instructions_text = QLabel(
            "<p>Este es tu panel de control como docente. Aquí podrás:</p>"
            "<ul>"
            "<li>Consultar la <b>lista de estudiantes</b> y sus datos</li>"
            "<li>Ver información sobre otros <b>profesores</b></li>"
            "<li>Revisar los <b>eventos</b> próximos y la asistencia mensual</li>"
            "</ul>"
            "<p>Utiliza la navegación de la izquierda para acceder a las diferentes secciones.</p>"
        )
        instructions_text.setWordWrap(True)
        instructions_text.setObjectName("instructions-text")
        instructions_text.setStyleSheet("color: #333333; font-size: 14px;")
        info_layout.addWidget(instructions_text)
        
        buttons_layout = QHBoxLayout()
        
        students_button = QPushButton("Ver Estudiantes")
        students_button.setObjectName("quick-access-button")
        students_button.clicked.connect(lambda: self._handle_navigation("estudiantes"))
        students_button.setStyleSheet("background-color: #3a7bd5; color: white; border: none; border-radius: 6px; padding: 10px 15px; font-weight: bold; font-size: 14px;")
        
        teachers_button = QPushButton("Ver Profesores")
        teachers_button.setObjectName("quick-access-button")
        teachers_button.clicked.connect(lambda: self._handle_navigation("profesores"))
        teachers_button.setStyleSheet("background-color: #3a7bd5; color: white; border: none; border-radius: 6px; padding: 10px 15px; font-weight: bold; font-size: 14px;")
        
        events_button = QPushButton("Ver Eventos")
        events_button.setObjectName("quick-access-button")
        events_button.clicked.connect(lambda: self._handle_navigation("eventos"))
        events_button.setStyleSheet("background-color: #3a7bd5; color: white; border: none; border-radius: 6px; padding: 10px 15px; font-weight: bold; font-size: 14px;")
        
        buttons_layout.addWidget(students_button)
        buttons_layout.addWidget(teachers_button)
        buttons_layout.addWidget(events_button)
        
        info_layout.addLayout(buttons_layout)
        home_layout.addWidget(info_frame)
        home_layout.addWidget(self._control_cards_container)
        home_layout.addStretch(1)
        
        # Create page for "estudiantes" tab
        students_page = QWidget()
        students_layout = QVBoxLayout(students_page)
        students_layout.addWidget(self._students_section)
        students_layout.addStretch(1)
        
        # Create page for "profesores" tab
        teachers_page = QWidget()
        teachers_layout = QVBoxLayout(teachers_page)
        teachers_layout.addWidget(self._teachers_section)
        teachers_layout.addStretch(1)
        
        # Create page for "eventos" tab
        events_page = QWidget()
        events_layout = QVBoxLayout(events_page)
        events_layout.addWidget(self._events_section)
        events_layout.addWidget(self._attendance_section)
        events_layout.addStretch(1)
        
        # Add all pages to the stack
        self._content_stack.addWidget(home_page)       # Index 0: inicio
        self._content_stack.addWidget(students_page)   # Index 1: estudiantes
        self._content_stack.addWidget(teachers_page)   # Index 2: profesores
        self._content_stack.addWidget(events_page)     # Index 3: eventos
        
        # Set initial page to estudiantes (matches default in _current_section)
        self._content_stack.setCurrentIndex(1)
        
        # Store the page indices for navigation
        self._page_indices = {
            "inicio": 0,
            "estudiantes": 1,
            "profesores": 2,
            "eventos": 3
        }
        
        # Add the stacked widget to the main layout
        self._main_layout.addWidget(self._content_stack, 1, 1, 5, 4)
        
        # Set column stretches
        self._main_layout.setColumnStretch(0, 0)  # Navigation doesn't stretch
        self._main_layout.setColumnStretch(1, 1)
        self._main_layout.setColumnStretch(2, 1)
        self._main_layout.setColumnStretch(3, 1)
        self._main_layout.setColumnStretch(4, 1)

        # Set row stretches
        self._main_layout.setRowStretch(0, 0)  # Header row doesn't stretch
        self._main_layout.setRowStretch(1, 1)  # Content area stretches

    def _apply_styles(self) -> None:
        """Apply styles to the dashboard"""
        # Main styles
        self._container.setStyleSheet("""
                #teacher-dashboard-container {
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

                /* Search bar */
                #search-bar {
                    border-radius: 3px;
                    padding: 8px;
                    border: 1px solid #ddd;
                    background-color: white;
                    margin: 10px;
                }

                /* User info */
                #user-info {
                    padding: 5px;
                }

                #user-icon {
                    font-size: 24px;
                }

                #user-name {
                    font-size: 14px;
                }

                #logout-button {
                    background-color: transparent;
                    color: #333;
                    border: none;
                }

                /* Control cards */
                #control-cards QFrame {
                    border-radius: 10px;
                    padding: 15px;
                    color: #333;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s ease;
                }

                #students-card {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                }

                #admin-card {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }

                #schedule-card {
                    background: linear-gradient(135deg, #13547a 0%, #80d0c7 100%);
                    color: white;
                }

                #students-card-arrow, #admin-card-arrow, #schedule-card-arrow {
                    font-size: 24px;
                    font-weight: bold;
                }

                /* Section titles */
                #section-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                }

                #view-all-link {
                    color: #4a86e8;
                    text-decoration: underline;
                    cursor: pointer;
                }

                /* Students table */
                #students-table {
                    border: none;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                }

                #students-table::item {
                    padding: 8px;
                    font-size: 14px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    color: #000000;
                }

                #students-table::item:selected {
                    background-color: #4facfe;
                    color: white;
                }
                
                #students-table {
                    color: #000000;
                }
                
                #welcome-container {
                    background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);
                    color: white;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }

                #students-table QHeaderView::section {
                    background-color: #3a7bd5;
                    color: white;
                    padding: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "Segoe UI", Arial, sans-serif;
                    border: none;
                }

                /* Events section */
                #events-section {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                    border: 1px solid #e0e0e0;
                }

                #events-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: #000000;
                }

                #events-icon {
                    font-size: 18px;
                    color: #000000;
                }

                #event-card {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #e0e0e0;
                }
                
                #event-time {
                    color: #000000;
                    font-weight: 500;
                    font-size: 13px;
                }

                #event-date {
                    background-color: #f0f0f0;
                    border-radius: 5px;
                    color: #333333;
                    padding: 5px;
                    border: 1px solid #e0e0e0;
                }

                #event-day, #event-date-number, #event-month {
                    font-weight: bold;
                    color: #333333;
                }

                #event-date-number {
                    font-size: 18px;
                }

                #event-title {
                    font-weight: bold;
                    color: #000000;
                    font-size: 15px;
                }

                #days-left {
                    color: #333333;
                    font-weight: 500;
                }

                /* Attendance chart */
                #attendance-section {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                    border: 1px solid #e0e0e0;
                }

                #attendance-bar {
                    background-color: #f0f0f0;
                    width: 30px;
                    border-radius: 3px 3px 0 0;
                    border: 1px solid #e0e0e0;
                }

                #attendance-color {
                    background-color: #f0f0f0;
                    border-radius: 3px;
                    border: 1px solid #e0e0e0;
                }

                #absence-color {
                    background-color: #ffffff;
                    border-radius: 3px;
                    border: 1px solid #e0e0e0;
                }

                /* Teachers section */
                #teachers-section {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                    border: 1px solid #e0e0e0;
                }

                #teacher-card {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                    border: 1px solid #e0e0e0;
                }

                #teacher-avatar {
                    font-size: 32px;
                    color: #333333;
                }

                #teacher-name {
                    font-weight: bold;
                    font-size: 15px;
                    color: #000000;
                }

                #teacher-subject {
                    color: #333333;
                    font-size: 13px;
                    font-weight: 500;
                }
            """)

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
            self._teacher_name,
            self._on_logout,
            self._on_navigate,
            self._student_viewmodel,
            self._teacher_viewmodel,
            self._event_viewmodel
        )

    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)

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
            
        # Switch to the appropriate tab using the stacked widget
        if section in self._page_indices:
            self._content_stack.setCurrentIndex(self._page_indices[section])
            self._logger.info(f"Switched to tab index {self._page_indices[section]} for section {section}")
                
        # Trigger data loading based on the selected section
        if section == "estudiantes" and self._student_viewmodel:
            self._student_viewmodel.load_students()
        elif section == "profesores" and self._teacher_viewmodel:
            self._teacher_viewmodel.load_teachers()
        elif section == "eventos" and self._event_viewmodel:
            self._event_viewmodel.load_upcoming_events()
            self._event_viewmodel.load_monthly_attendance()

        # Call external navigation handler if provided
        self._on_navigate(section)

        # Log navigation
        self._logger.info(f"Navigated to section: {section}")

    def _handle_search(self) -> None:
        """Handle search action"""
        search_text = self._search_bar.text().strip()
        if not search_text:
            return

        self._logger.info(f"Searching for: {search_text}")

        # You would normally filter the students table or other content here
        # For demonstration purposes, we're just printing the search term
        self._search_bar.clear()

    def _handle_view_all_students(self) -> None:
        """Handle view all students action"""
        print("Viewing all students")
        self._handle_navigation("estudiantes")

    def _handle_student_selected(self, row: int, column: int) -> None:
        """Handle student selection from the table

        :param row: Selected row
        :param column: Selected column
        """
        student_name = self._students_table.item(row, 0).text()
        print(f"Student selected: {student_name}")

        # Notify the application coordinator to show student details
        if hasattr(self, '_on_navigate') and self._on_navigate:
            # Call with a special format to indicate student details
            self._on_navigate(f"student_details:{student_name}")

    def _handle_view_all_attendance(self) -> None:
        """Handle view all attendance action"""
        print("Viewing all attendance records")
        # This would typically show a detailed attendance view

    def _handle_view_all_teachers(self) -> None:
        """Handle view all teachers action"""
        print("Viewing all teachers")
        self._handle_navigation("profesores")

    def _handle_teacher_selected(self, teacher_name: str) -> None:
        """Handle teacher selection

        :param teacher_name: Name of the selected teacher
        """
        print(f"Teacher selected: {teacher_name}")

        # Notify the application coordinator to show teacher details
        if hasattr(self, '_on_navigate') and self._on_navigate:
            # Call with a special format to indicate teacher details
            self._on_navigate(f"teacher_details:{teacher_name}")
            
    def _on_students_loaded(self, students) -> None:
        """Handle students loaded signal from student viewmodel
        
        :param students: List of loaded students
        """
        self._logger.info(f"Students loaded: {len(students) if students else 0}")
        
        # Update the UI with the loaded students
        if hasattr(self, '_students_table') and self._students_table:
            # Clear existing rows
            self._students_table.setRowCount(0)
            
            if students:
                # Add new rows for each student
                self._students_table.setRowCount(len(students))
                
                for row, student in enumerate(students):
                    # Extract name, grade and attendance
                    name = f"{student.get('first_name', '')} {student.get('last_name', '')}"
                    grade = student.get('grade_level', 'N/A')
                    attendance = f"{student.get('attendance_rate', 'N/A')}%"
                    
                    name_item = QTableWidgetItem(name)
                    name_item.setData(Qt.UserRole, student.get('uuid', ''))
                    
                    self._students_table.setItem(row, 0, name_item)
                    self._students_table.setItem(row, 1, QTableWidgetItem(str(grade)))
                    self._students_table.setItem(row, 2, QTableWidgetItem(str(attendance)))
                    
    def _on_monthly_attendance_loaded(self, attendance_data: dict) -> None:
        """Handle monthly attendance data loaded signal from event viewmodel
        
        :param attendance_data: Dictionary with month names as keys and attendance percentages as values
        """
        self._logger.info(f"Monthly attendance data loaded: {attendance_data}")
        
        # Update the attendance chart with the loaded data
        if hasattr(self, '_chart_layout') and attendance_data:
            # Clear existing bars
            while self._chart_layout.count() > 0:
                item = self._chart_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Sort months to ensure chronological order (Ene, Feb, Mar, etc.)
            # We'll create a custom sort key function based on Spanish month abbreviations
            month_order = {"Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, 
                          "Jun": 6, "Jul": 7, "Ago": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12}
            
            # Sort the months by their numerical order
            sorted_months = sorted(attendance_data.items(), key=lambda x: month_order.get(x[0], 13))
            
            # Create new bars
            for month, value in sorted_months:
                bar_container = QFrame()
                bar_container.setFixedWidth(60)
                bar_layout = QVBoxLayout()
                bar_container.setLayout(bar_layout)
                
                # Value label (percentage)
                value_label = QLabel(f"{value}%")
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 13px;")
                
                # Apply color based on value
                if value >= 90:
                    color = "#4CAF50"  # Green for excellent
                elif value >= 80:
                    color = "#2196F3"  # Blue for good
                elif value >= 70:
                    color = "#FF9800"  # Orange for average
                else:
                    color = "#F44336"  # Red for poor
                
                # Bar with color based on value
                bar = QFrame()
                bar.setObjectName("attendance-bar")
                bar.setFixedHeight(int(value * 1.8))  # Scale value to height
                bar.setStyleSheet(f"""
                    #attendance-bar {{
                        background-color: {color};
                        border-radius: 4px;
                    }}
                """)
                
                # Month label
                month_label = QLabel(month)
                month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                month_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 13px;")
                
                # Add widgets to layout with proper spacing
                bar_layout.addWidget(value_label)
                bar_layout.addSpacing(5)
                bar_layout.addStretch(1)  # Push bar to bottom
                bar_layout.addWidget(bar)
                bar_layout.addSpacing(5)
                bar_layout.addWidget(month_label)
                
                self._chart_layout.addWidget(bar_container)
    
    def _on_teachers_loaded(self, teachers) -> None:
        """Handle teachers loaded signal from teacher viewmodel
        
        :param teachers: List of loaded teachers
        """
        self._logger.info(f"Teachers loaded: {len(teachers) if teachers else 0}")
        
        # Update the teachers section with data from the API
        # First clear the current teacher list by removing all widgets
        if hasattr(self, '_teachers_section'):
            # Get the layout
            teachers_layout = self._teachers_section.layout()
            if teachers_layout:
                # Find the horizontal layout containing teacher cards
                for i in range(teachers_layout.count()):
                    item = teachers_layout.itemAt(i)
                    if isinstance(item, QHBoxLayout):
                        # Clear all widgets from this horizontal layout
                        while item.count() > 0:
                            widget = item.takeAt(0).widget()
                            if widget:
                                widget.deleteLater()
                        
                        # Now add new teacher cards
                        if teachers:
                            for teacher in teachers[:4]:  # Limit to 4 teachers to fit the UI nicely
                                name = f"{teacher.get('first_name', '')} {teacher.get('last_name', '')}"
                                specialization = teacher.get('specialization', 'General')
                                
                                # Create teacher card
                                teacher_card = QFrame()
                                teacher_card.setObjectName("teacher-card")
                                
                                card_layout = QVBoxLayout()
                                teacher_card.setLayout(card_layout)
                                
                                # Create circular profile image
                                initials = get_initials(name)
                                avatar = CircularImageWidget(size=60, placeholder_bg_color="#8ecaef", placeholder_text=initials)
                                avatar.setObjectName("teacher-avatar")
                                
                                # Try to load profile image
                                # Extract teacher_id properly as a string
                                teacher_id = str(teacher.get('uuid', name.lower().replace(" ", "_")))
                                image_path = self._profile_image_service.get_image_path(teacher_id, "teacher")
                                avatar.setImage(image_path)
                                
                                # Name label (clickable)
                                name_label = QLabel(name)
                                name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                name_label.setObjectName("teacher-name")
                                name_label.setCursor(Qt.CursorShape.PointingHandCursor)
                                
                                # Create a proper mouse event handler
                                teacher_name = name  # Capture the current teacher name
                                orig_mouse_press = name_label.mousePressEvent
                                
                                def new_mouse_press(event, t=teacher_name):
                                    self._handle_teacher_selected(t)
                                    if orig_mouse_press:
                                        orig_mouse_press(event)
                                
                                name_label.mousePressEvent = new_mouse_press
                                
                                # Subject/specialization
                                subject_label = QLabel(specialization)
                                subject_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                subject_label.setObjectName("teacher-subject")
                                
                                card_layout.addWidget(avatar)
                                card_layout.addWidget(name_label)
                                card_layout.addWidget(subject_label)
                                
                                item.addWidget(teacher_card)
                        break
        
    def _on_events_loaded(self, events) -> None:
        """Handle events loaded signal from event viewmodel
        
        :param events: List of loaded events
        """
        self._logger.info(f"Events loaded: {len(events) if events else 0}")
        
        # Update events section with the loaded events
        if hasattr(self, '_events_section') and events:
            # Get the layout
            events_layout = self._events_section.layout()
            if events_layout:
                # Clear existing event cards
                # Find all event cards and remove them
                items_to_remove = []
                for i in range(events_layout.count()):
                    layout_item = events_layout.itemAt(i)
                    if layout_item:
                        widget = layout_item.widget()
                        if widget and widget.objectName() == "event-card":
                            items_to_remove.append(widget)
                
                # Remove the identified widgets
                for widget in items_to_remove:
                    widget.deleteLater()
                
                # Format events for display
                if self._event_viewmodel:
                    formatted_events = self._event_viewmodel.format_upcoming_events_for_display()
                    
                    # Add new event cards for each event
                    for weekday, date, title, time_str, days_left in formatted_events[:3]:  # Show only 3 most recent
                        self._create_event_card(weekday, date, title, time_str, days_left, events_layout)
        
    def _get_student_data(self) -> List[Tuple[str, str, str]]:
        """Get student data for displaying in the table
        
        :return: List of (name, grade, attendance) tuples
        """
        # Try to get data from the viewmodel if available
        if self._student_viewmodel:
            try:
                # Trigger data loading if not already loaded
                self._student_viewmodel.load_students()
                
                # Return empty list for now as data will come through the signal
                return []
            except Exception as e:
                self._logger.error(f"Error loading students from viewmodel: {e}")
                
        # Fallback to dummy data if viewmodel is not available or failed
        return [
            ("Alex Johnson", "10° grado", "95%"),
            ("Maria Garcia", "11° grado", "89%"),
            ("Carlos Rodriguez", "10° grado", "91%"),
            ("Emma Wilson", "11° grado", "87%"),
        ]
        
    def _get_teacher_data(self) -> List[Tuple[str, str]]:
        """Get teacher data for displaying in the cards
        
        :return: List of (name, subject) tuples
        """
        # Try to get data from the viewmodel if available
        if self._teacher_viewmodel:
            try:
                # Trigger data loading if not already loaded
                self._teacher_viewmodel.load_teachers()
                
                # Return empty list for now as data will come through the signal
                return []
            except Exception as e:
                self._logger.error(f"Error loading teachers from viewmodel: {e}")
                
        # Fallback to dummy data if viewmodel is not available or failed
        return [
            ("Laura Gómez", "Matemáticas"),
            ("David Martinez", "Ciencias"),
            ("Sara López", "Literatura"),
            ("Miguel Torres", "Historia")
        ]