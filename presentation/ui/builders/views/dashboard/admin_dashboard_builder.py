import logging
from typing import Callable, Dict, Optional, List, Tuple, Any
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, QFrame,
                               QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout, QVBoxLayout, QScrollArea, QStackedWidget,
                               QComboBox, QDialog, QFormLayout, QDialogButtonBox)

from presentation.ui.viewmodels import UserViewModel, ReportViewModel
from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.widgets import CircularImageWidget, get_initials
from domain.entities.user import UserRole
from domain.services.profile_image_service import ProfileImageService


class AdminDashboardBuilder(Builder):
    """
    Builder for the admin dashboard view that shows user management, reports and class assignments
    """

    def __init__(
            self,
            wf: WidgetFactory,
            lf: LayoutFactory,
            admin_name: str,
            on_logout: Callable[[], None] = None,
            on_navigate: Callable[[str], None] = None,
            user_viewmodel: Optional[UserViewModel] = None,
            report_viewmodel: Optional[ReportViewModel] = None
    ):
        """
        Initialize the admin dashboard builder

        :param wf: Widget factory
        :param lf: Layout factory
        :param admin_name: Admin name to display
        :param on_logout: Callback for logout action
        :param on_navigate: Callback for navigation
        :param user_viewmodel: ViewModel for user management
        :param report_viewmodel: ViewModel for reports
        """
        self._wf = wf
        self._lf = lf
        self._admin_name = admin_name
        self._on_logout = on_logout or (lambda: None)
        self._on_navigate = on_navigate or (lambda section: None)
        self._user_viewmodel = user_viewmodel
        self._report_viewmodel = report_viewmodel

        # Profile image service to handle profile images
        self._profile_image_service = ProfileImageService()

        # Current view/section
        self._current_section = "usuarios"

        # Logger for this class
        self._logger = logging.getLogger(__name__)
        
        # Connect to viewmodel signals if available
        if self._user_viewmodel:
            self._user_viewmodel.usersLoaded.connect(self._on_users_loaded)
            self._user_viewmodel.userAdded.connect(self._on_user_added)
            self._user_viewmodel.userUpdated.connect(self._on_user_updated)
            # Trigger initial data load
            QTimer.singleShot(100, self._user_viewmodel.load_users)
            
        if self._report_viewmodel:
            self._report_viewmodel.reportGenerated.connect(self._on_report_generated)
            # Add listener for reports loaded
            self._report_viewmodel.reportsLoaded.connect(self._on_reports_loaded)
            
            # Trigger initial data load
            QTimer.singleShot(200, self._report_viewmodel.load_reports)

        # Create container widget
        self._container = QWidget()
        self._container.setObjectName("admin-dashboard-container")

        # Main layout
        self._main_layout = QGridLayout()
        self._container.setLayout(self._main_layout)

        # Create components
        self._create_left_navigation()
        self._create_welcome_banner()
        self._create_users_section()
        self._create_reports_section()
        self._create_assignments_section()
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
            ("Usuarios", "usuarios"),
            ("Reportes", "reportes"),
            ("Asignaciones", "asignaciones"),
            ("Configuración", "configuracion")
        ]

        self._nav_buttons = {}
        for label, item_id in nav_items:
            btn = QPushButton(label)
            btn.setObjectName(f"nav-{item_id}")
            btn.setCheckable(True)

            # Set usuarios as active by default
            if item_id == "usuarios":
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
        
        welcome_message = QLabel(f"¡Bienvenido, {self._admin_name}!")
        welcome_message.setObjectName("welcome-message")
        
        welcome_description = QLabel("Administra usuarios, genera reportes y gestiona asignaciones de materias y profesores")
        welcome_description.setObjectName("welcome-description")
        
        welcome_text_container.addWidget(welcome_message)
        welcome_text_container.addWidget(welcome_description)
        welcome_text_container.addStretch(1)
        
        # Action button
        action_button = QPushButton("Gestionar Usuarios")
        action_button.setObjectName("action-button")
        action_button.clicked.connect(lambda: self._handle_navigation("usuarios"))
        welcome_text_container.addWidget(action_button)
        
        # Admin image
        admin_image = QLabel("👨‍💼")
        admin_image.setObjectName("admin-image")
        admin_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addLayout(welcome_text_container, 2)
        welcome_layout.addWidget(admin_image, 1)
        
    def _create_users_section(self) -> None:
        """Create users management section"""
        # Section container
        self._users_section = QFrame()
        self._users_section.setObjectName("users-section")

        users_layout = QVBoxLayout()
        self._users_section.setLayout(users_layout)

        # Header with title and add button
        header_layout = QHBoxLayout()

        self._users_title = QLabel("Gestión de Usuarios")
        self._users_title.setObjectName("section-title")
        
        add_user_button = QPushButton("+ Nuevo Usuario")
        add_user_button.setObjectName("add-button")
        add_user_button.clicked.connect(self._handle_add_user)
        
        header_layout.addWidget(self._users_title)
        header_layout.addStretch(1)
        header_layout.addWidget(add_user_button)

        users_layout.addLayout(header_layout)

        # Filter controls
        filter_layout = QHBoxLayout()
        
        role_filter_label = QLabel("Filtrar por rol:")
        role_filter_label.setStyleSheet("color: #000000;")
        
        self._role_filter = QComboBox()
        self._role_filter.addItems(["Todos", "Administrador", "Profesor", "Estudiante"])
        self._role_filter.currentTextChanged.connect(self._handle_role_filter_changed)
        
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Buscar por nombre...")
        search_bar.textChanged.connect(self._handle_user_search)
        
        filter_layout.addWidget(role_filter_label)
        filter_layout.addWidget(self._role_filter)
        filter_layout.addStretch(1)
        filter_layout.addWidget(search_bar)
        
        users_layout.addLayout(filter_layout)

        # Create users table
        self._users_table = QTableWidget()
        self._users_table.setObjectName("users-table")
        self._users_table.setColumnCount(5)
        self._users_table.setHorizontalHeaderLabels(["Nombre", "Email", "Rol", "Estado", "Acciones"])
        
        # Set header text color directly
        header_view = self._users_table.horizontalHeader()
        header_view.setStyleSheet("QHeaderView::section { color: white; font-weight: bold; }")

        # Configure table appearance
        self._users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._users_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._users_table.setAlternatingRowColors(True)
        self._users_table.setShowGrid(True)
        self._users_table.setGridStyle(Qt.PenStyle.SolidLine)
        self._users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Get users data from API (via view model)
        users_data = self._get_users_data()
        self._populate_users_table(users_data)

        users_layout.addWidget(self._users_table)
        
    def _populate_users_table(self, users_data: List[Dict[str, Any]]) -> None:
        """
        Populate users table with data
        
        :param users_data: List of user data dictionaries
        """
        self._users_table.setRowCount(len(users_data))
        
        for row, user in enumerate(users_data):
            name_item = QTableWidgetItem(user.get("name", ""))
            email_item = QTableWidgetItem(user.get("email", ""))
            role_item = QTableWidgetItem(user.get("role", ""))
            
            status = user.get("active", True)
            status_text = "Activo" if status else "Inactivo"
            status_item = QTableWidgetItem(status_text)
            
            # Set colors for status
            if status:
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.darkRed)
                
            # Set items in table
            self._users_table.setItem(row, 0, name_item)
            self._users_table.setItem(row, 1, email_item)
            self._users_table.setItem(row, 2, role_item)
            self._users_table.setItem(row, 3, status_item)
            
            # Actions cell with edit and delete buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setToolTip("Editar usuario")
            edit_btn.setFixedSize(30, 25)
            edit_btn.setStyleSheet("background-color: #f0f0f0; border: none;")
            edit_btn.clicked.connect(lambda _, u=user: self._handle_edit_user(u))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Eliminar usuario")
            delete_btn.setFixedSize(30, 25)
            delete_btn.setStyleSheet("background-color: #f0f0f0; border: none;")
            delete_btn.clicked.connect(lambda _, u=user: self._handle_delete_user(u))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch(1)
            
            self._users_table.setCellWidget(row, 4, actions_widget)
        
    def _create_reports_section(self) -> None:
        """Create reports generation section"""
        # Section container
        self._reports_section = QFrame()
        self._reports_section.setObjectName("reports-section")

        reports_layout = QVBoxLayout()
        self._reports_section.setLayout(reports_layout)

        # Header with title
        header_layout = QHBoxLayout()

        self._reports_title = QLabel("Generación de Reportes")
        self._reports_title.setObjectName("section-title")
        
        header_layout.addWidget(self._reports_title)
        header_layout.addStretch(1)

        reports_layout.addLayout(header_layout)
        
        # Report types
        report_types_layout = QGridLayout()
        
        report_types = [
            {"name": "Asistencia", "icon": "📊", "description": "Reporte de asistencia por clase"},
            {"name": "Calificaciones", "icon": "📝", "description": "Reporte de calificaciones por alumno"},
            {"name": "Horarios", "icon": "🕒", "description": "Reporte de horarios por profesor"},
            {"name": "Usuarios", "icon": "👥", "description": "Reporte de usuarios registrados"}
        ]
        
        row, col = 0, 0
        for report in report_types:
            report_card = self._create_report_card(report)
            report_types_layout.addWidget(report_card, row, col)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        reports_layout.addLayout(report_types_layout)
        
        # Recent reports
        recent_title = QLabel("Reportes recientes")
        recent_title.setObjectName("subsection-title")
        recent_title.setStyleSheet("font-weight: bold; color: #000000; font-size: 16px;")
        
        reports_layout.addWidget(recent_title)
        
        # Recent reports table
        self._recent_reports_table = QTableWidget()
        self._recent_reports_table.setObjectName("recent-reports-table")
        self._recent_reports_table.setColumnCount(3)
        self._recent_reports_table.setHorizontalHeaderLabels(["Nombre", "Fecha", "Descargar"])
        
        # Configure table appearance
        self._recent_reports_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._recent_reports_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._recent_reports_table.setAlternatingRowColors(True)
        self._recent_reports_table.setShowGrid(True)
        
        # Mock data for recent reports
        recent_reports = [
            {"name": "Reporte de Asistencia - Agosto 2025", "date": "01/08/2025"},
            {"name": "Reporte de Calificaciones - Semestre 2025-1", "date": "29/07/2025"},
            {"name": "Reporte de Usuarios Nuevos", "date": "25/07/2025"}
        ]
        
        self._recent_reports_table.setRowCount(len(recent_reports))
        for row, report in enumerate(recent_reports):
            self._recent_reports_table.setItem(row, 0, QTableWidgetItem(report["name"]))
            self._recent_reports_table.setItem(row, 1, QTableWidgetItem(report["date"]))
            
            # Download button
            download_widget = QWidget()
            download_layout = QHBoxLayout(download_widget)
            download_layout.setContentsMargins(4, 2, 4, 2)
            
            download_btn = QPushButton("📥")
            download_btn.setFixedSize(30, 25)
            download_btn.setStyleSheet("background-color: #f0f0f0; border: none;")
            download_btn.clicked.connect(lambda _, r=report: self._handle_download_report(r))
            
            download_layout.addWidget(download_btn)
            download_layout.addStretch(1)
            
            self._recent_reports_table.setCellWidget(row, 2, download_widget)
            
        reports_layout.addWidget(self._recent_reports_table)
        
    def _create_report_card(self, report: Dict[str, str]) -> QFrame:
        """
        Create a report type card
        
        :param report: Report type information
        :return: Card widget
        """
        card = QFrame()
        card.setObjectName("report-card")
        
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        
        # Icon and name
        header_layout = QHBoxLayout()
        
        icon = QLabel(report["icon"])
        icon.setObjectName("report-icon")
        icon.setStyleSheet("font-size: 24px;")
        
        name = QLabel(report["name"])
        name.setObjectName("report-name")
        name.setStyleSheet("font-weight: bold; color: #000000; font-size: 16px;")
        
        header_layout.addWidget(icon)
        header_layout.addWidget(name)
        header_layout.addStretch(1)
        
        # Description
        description = QLabel(report["description"])
        description.setObjectName("report-description")
        description.setStyleSheet("color: #333333;")
        description.setWordWrap(True)
        
        # Generate button
        generate_btn = QPushButton("Generar")
        generate_btn.setObjectName("generate-button")
        generate_btn.clicked.connect(lambda _, r=report: self._handle_generate_report(r))
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(description)
        card_layout.addWidget(generate_btn)
        
        return card
        
    def _create_assignments_section(self) -> None:
        """Create class assignments section"""
        # Section container
        self._assignments_section = QFrame()
        self._assignments_section.setObjectName("assignments-section")

        assignments_layout = QVBoxLayout()
        self._assignments_section.setLayout(assignments_layout)

        # Header with title and add button
        header_layout = QHBoxLayout()

        self._assignments_title = QLabel("Asignación de Materias y Profesores")
        self._assignments_title.setObjectName("section-title")
        
        add_assignment_button = QPushButton("+ Nueva Asignación")
        add_assignment_button.setObjectName("add-button")
        add_assignment_button.clicked.connect(self._handle_add_assignment)
        
        header_layout.addWidget(self._assignments_title)
        header_layout.addStretch(1)
        header_layout.addWidget(add_assignment_button)

        assignments_layout.addLayout(header_layout)
        
        # Create assignments table
        self._assignments_table = QTableWidget()
        self._assignments_table.setObjectName("assignments-table")
        self._assignments_table.setColumnCount(5)
        self._assignments_table.setHorizontalHeaderLabels(["Materia", "Profesor", "Horario", "Aula", "Acciones"])
        
        # Set header text color directly
        header_view = self._assignments_table.horizontalHeader()
        header_view.setStyleSheet("QHeaderView::section { color: white; font-weight: bold; }")

        # Configure table appearance
        self._assignments_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._assignments_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._assignments_table.setAlternatingRowColors(True)
        self._assignments_table.setShowGrid(True)
        
        # Mock data for assignments
        assignments = [
            {"subject": "Matemáticas", "teacher": "Laura Gómez", "schedule": "Lun 8:00-10:00", "room": "A101"},
            {"subject": "Historia", "teacher": "Miguel Torres", "schedule": "Mar 10:00-12:00", "room": "A102"},
            {"subject": "Física", "teacher": "David Martinez", "schedule": "Lun/Mie 12:00-14:00", "room": "B201"},
            {"subject": "Literatura", "teacher": "Carmen Vega", "schedule": "Mie 8:00-10:00", "room": "A103"},
            {"subject": "Inglés", "teacher": "Sarah Johnson", "schedule": "Lun 16:00-18:00", "room": "C301"}
        ]
        
        self._assignments_table.setRowCount(len(assignments))
        for row, assignment in enumerate(assignments):
            self._assignments_table.setItem(row, 0, QTableWidgetItem(assignment["subject"]))
            self._assignments_table.setItem(row, 1, QTableWidgetItem(assignment["teacher"]))
            self._assignments_table.setItem(row, 2, QTableWidgetItem(assignment["schedule"]))
            self._assignments_table.setItem(row, 3, QTableWidgetItem(assignment["room"]))
            
            # Actions cell with edit and delete buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 25)
            edit_btn.setStyleSheet("background-color: #f0f0f0; border: none;")
            edit_btn.clicked.connect(lambda _, a=assignment: self._handle_edit_assignment(a))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 25)
            delete_btn.setStyleSheet("background-color: #f0f0f0; border: none;")
            delete_btn.clicked.connect(lambda _, a=assignment: self._handle_delete_assignment(a))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch(1)
            
            self._assignments_table.setCellWidget(row, 4, actions_widget)
            
        assignments_layout.addWidget(self._assignments_table)

    def _create_user_info(self) -> None:
        """Create user info section in header"""
        self._user_info = QFrame()
        self._user_info.setObjectName("user-info")

        info_layout = QHBoxLayout()
        self._user_info.setLayout(info_layout)

        # Get user initials for placeholder
        initials = get_initials(self._admin_name)

        # Create circular profile image
        self._profile_image = CircularImageWidget(
            size=40,
            placeholder_bg_color="#5a7a95",
            placeholder_text=initials
        )
        self._profile_image.setObjectName("profile-image")

        # Try to load profile image if available
        admin_id = self._admin_name.lower().replace(" ", "_")
        image_path = self._profile_image_service.get_image_path(admin_id, "admin")
        self._profile_image.setImage(image_path)

        # User name
        user_name = QLabel(f"Nombre de Usuario: {self._admin_name}")
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

        # Third row: users section
        self._main_layout.addWidget(self._users_section, 2, 1, 1, 3)

        # Fourth row: reports and assignments sections
        self._main_layout.addWidget(self._reports_section, 3, 1, 1, 1)
        self._main_layout.addWidget(self._assignments_section, 3, 2, 1, 2)

        # Set column and row stretches
        self._main_layout.setColumnStretch(0, 0)  # Navigation doesn't stretch
        self._main_layout.setColumnStretch(1, 1)
        self._main_layout.setColumnStretch(2, 1)
        self._main_layout.setColumnStretch(3, 1)

        self._main_layout.setRowStretch(0, 0)  # Header row doesn't stretch
        self._main_layout.setRowStretch(1, 0)  # Welcome banner doesn't stretch
        self._main_layout.setRowStretch(2, 2)  # Users section stretches more
        self._main_layout.setRowStretch(3, 1)  # Reports and assignments stretch less

    def _apply_styles(self) -> None:
        """Apply styles to the dashboard"""
        # Main styles
        self._container.setStyleSheet("""
                #admin-dashboard-container {
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
                
                #admin-image {
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
                #users-section, #reports-section, #assignments-section {
                    background-color: white;
                    border-radius: 8px;
                    padding: 15px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    border: 1px solid #e0e0e0;
                    margin-bottom: 15px;
                }
                
                #section-title {
                    font-size: 22px;
                    font-weight: bold;
                    color: #3a7bd5;
                    margin-bottom: 15px;
                    font-family: "Segoe UI", Arial, sans-serif;
                }

                /* Tables */
                #users-table, #assignments-table, #recent-reports-table {
                    border: none;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    color: #000000;
                }

                #users-table::item, #assignments-table::item, #recent-reports-table::item {
                    padding: 8px;
                    font-size: 14px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    color: #000000;
                }

                #users-table::item:selected, #assignments-table::item:selected, #recent-reports-table::item:selected {
                    background-color: #4facfe;
                    color: white;
                }
                
                /* Buttons */
                #add-button, #generate-button {
                    background-color: #3a7bd5;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-weight: bold;
                    transition: background-color 0.2s;
                }
                
                #add-button:hover, #generate-button:hover {
                    background-color: #2a6bc5;
                }
                
                /* Report cards */
                #report-card {
                    background-color: white;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    border: 1px solid #e0e0e0;
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

    def _get_users_data(self) -> List[Dict[str, Any]]:
        """Get users data for displaying in the table
        
        :return: List of user data dictionaries
        """
        # Try to get data from the viewmodel if available
        if self._user_viewmodel:
            try:
                # Trigger data loading if not already loaded
                self._user_viewmodel.load_users()
                
                # Return empty list for now as data will come through the signal
                return []
            except Exception as e:
                self._logger.error(f"Error loading users from viewmodel: {e}")
                
        # Fallback to dummy data if viewmodel is not available or failed
        return [
            {"id": "usr-001", "name": "Admin Test", "email": "admin@test.com", "role": "Administrador", "active": True},
            {"id": "usr-002", "name": "Laura Gómez", "email": "laura.gomez@uamitos.edu.mx", "role": "Profesor", "active": True},
            {"id": "usr-003", "name": "David Martinez", "email": "david.martinez@uamitos.edu.mx", "role": "Profesor", "active": True},
            {"id": "usr-004", "name": "Miguel Torres", "email": "miguel.torres@uamitos.edu.mx", "role": "Profesor", "active": True},
            {"id": "usr-005", "name": "Ana García", "email": "ana.garcia@uamitos.edu.mx", "role": "Estudiante", "active": True},
            {"id": "usr-006", "name": "Carlos López", "email": "carlos.lopez@uamitos.edu.mx", "role": "Estudiante", "active": True},
            {"id": "usr-007", "name": "Maria Rodríguez", "email": "maria.rodriguez@uamitos.edu.mx", "role": "Estudiante", "active": False}
        ]
        
    def _handle_role_filter_changed(self, role: str) -> None:
        """Handle role filter change
        
        :param role: Selected role filter
        """
        # This would filter the users table based on the selected role
        self._logger.info(f"Role filter changed to {role}")
        
        if self._user_viewmodel:
            # Reset search filter and request filtered data
            self._user_viewmodel.set_role_filter(role)
            self._user_viewmodel.load_users()
            
    def _handle_user_search(self, search_text: str) -> None:
        """Handle user search
        
        :param search_text: Search text
        """
        # This would filter the users table based on the search text
        self._logger.info(f"Searching for users matching '{search_text}'")
        
        if self._user_viewmodel:
            # Set search filter and request filtered data
            self._user_viewmodel.set_search_filter(search_text)
            self._user_viewmodel.load_users()
            
    def _handle_add_user(self) -> None:
        """Handle add user action"""
        self._logger.info("Add user button clicked")
        # This would open a dialog to add a new user
        
        # In a real implementation, you would create a form dialog
        # Here's a simplified example:
        dialog = QDialog(self._container)
        dialog.setWindowTitle("Agregar Nuevo Usuario")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        email_input = QLineEdit()
        role_input = QComboBox()
        role_input.addItems(["Administrador", "Profesor", "Estudiante"])
        
        layout.addRow("Nombre:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Rol:", role_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Create new user
            user_data = {
                "name": name_input.text(),
                "email": email_input.text(),
                "role": role_input.currentText(),
                "active": True
            }
            
            if self._user_viewmodel:
                self._user_viewmodel.add_user(user_data)
            else:
                self._logger.info(f"Would add user: {user_data}")
                
    def _handle_edit_user(self, user: Dict[str, Any]) -> None:
        """Handle edit user action
        
        :param user: User data to edit
        """
        self._logger.info(f"Edit user button clicked for {user.get('name')}")
        # This would open a dialog to edit the user
        
    def _handle_delete_user(self, user: Dict[str, Any]) -> None:
        """Handle delete user action
        
        :param user: User data to delete
        """
        self._logger.info(f"Delete user button clicked for {user.get('name')}")
        # This would prompt for confirmation before deleting the user
        
    def _handle_generate_report(self, report: Dict[str, str]) -> None:
        """Handle generate report action
        
        :param report: Report type information
        """
        self._logger.info(f"Generate report button clicked for {report.get('name')}")
        # This would trigger report generation
        
        if self._report_viewmodel:
            self._report_viewmodel.generate_report(report.get("name", ""))
            
    def _handle_download_report(self, report: Dict[str, str]) -> None:
        """Handle download report action
        
        :param report: Report information
        """
        self._logger.info(f"Download report button clicked for {report.get('name')}")
        # This would trigger report download
        
    def _handle_add_assignment(self) -> None:
        """Handle add assignment action"""
        self._logger.info("Add assignment button clicked")
        # This would open a dialog to add a new assignment
        
    def _handle_edit_assignment(self, assignment: Dict[str, str]) -> None:
        """Handle edit assignment action
        
        :param assignment: Assignment data to edit
        """
        self._logger.info(f"Edit assignment button clicked for {assignment.get('subject')}")
        # This would open a dialog to edit the assignment
        
    def _handle_delete_assignment(self, assignment: Dict[str, str]) -> None:
        """Handle delete assignment action
        
        :param assignment: Assignment data to delete
        """
        self._logger.info(f"Delete assignment button clicked for {assignment.get('subject')}")
        # This would prompt for confirmation before deleting the assignment
        
    def _on_users_loaded(self, users) -> None:
        """Handle users loaded signal from user viewmodel
        
        :param users: List of loaded users
        """
        self._logger.info(f"Users loaded: {len(users) if users else 0}")
        
        # Update the UI with the loaded users
        if users:
            self._populate_users_table(users)
            
    def _on_user_added(self, user) -> None:
        """Handle user added signal from user viewmodel
        
        :param user: Added user data
        """
        self._logger.info(f"User added: {user.get('name')}")
        # Refresh the users table
        if self._user_viewmodel:
            self._user_viewmodel.load_users()
            
    def _on_user_updated(self, user) -> None:
        """Handle user updated signal from user viewmodel
        
        :param user: Updated user data
        """
        self._logger.info(f"User updated: {user.get('name')}")
        # Refresh the users table
        if self._user_viewmodel:
            self._user_viewmodel.load_users()
            
    def _on_reports_loaded(self, reports) -> None:
        """Handle reports loaded signal from report viewmodel
        
        :param reports: List of report data
        """
        self._logger.info(f"Reports loaded: {len(reports) if reports else 0}")
        
        # Update the reports table if it exists
        if hasattr(self, '_reports_table') and self._reports_table:
            # Clear existing rows
            self._reports_table.setRowCount(0)
            
            # Add new rows for each report
            if reports:
                self._reports_table.setRowCount(len(reports))
                
                for row, report in enumerate(reports):
                    # Report name
                    name_item = QTableWidgetItem(report.get('name', 'Reporte'))
                    self._reports_table.setItem(row, 0, name_item)
                    
                    # Report date
                    date_item = QTableWidgetItem(report.get('date', '-'))
                    self._reports_table.setItem(row, 1, date_item)
                    
                    # Status
                    status_item = QTableWidgetItem(report.get('status', 'Completado'))
                    self._reports_table.setItem(row, 2, status_item)
            
    def _on_report_generated(self, report) -> None:
        """Handle report generated signal from report viewmodel
        
        :param report: Generated report data
        """
        self._logger.info(f"Report generated: {report.get('name')}")
        # Update the recent reports table if it exists
        if hasattr(self, '_reports_table') and self._reports_table:
            # Add the new report to the top of the table
            self._reports_table.insertRow(0)
            
            # Report name
            name_item = QTableWidgetItem(report.get('name', 'Reporte'))
            self._reports_table.setItem(0, 0, name_item)
            
            # Report date
            date_item = QTableWidgetItem(report.get('date', '-'))
            self._reports_table.setItem(0, 1, date_item)
            
            # Status
            status_item = QTableWidgetItem(report.get('status', 'Completado'))
            self._reports_table.setItem(0, 2, status_item)
                
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
        if section == "usuarios":
            if hasattr(self, '_users_section'):
                self._users_section.setVisible(True)
            if hasattr(self, '_reports_section'):
                self._reports_section.setVisible(False)
            if hasattr(self, '_assignments_section'):
                self._assignments_section.setVisible(False)
        elif section == "reportes":
            if hasattr(self, '_users_section'):
                self._users_section.setVisible(False)
            if hasattr(self, '_reports_section'):
                self._reports_section.setVisible(True)
            if hasattr(self, '_assignments_section'):
                self._assignments_section.setVisible(False)
        elif section == "asignaciones":
            if hasattr(self, '_users_section'):
                self._users_section.setVisible(False)
            if hasattr(self, '_reports_section'):
                self._reports_section.setVisible(False)
            if hasattr(self, '_assignments_section'):
                self._assignments_section.setVisible(True)
                
        # Trigger data loading based on the selected section
        if section == "usuarios" and self._user_viewmodel:
            self._user_viewmodel.load_users()
        elif section == "reportes" and self._report_viewmodel:
            # Just load reports, don't try to connect to a handler that doesn't exist
            self._report_viewmodel.load_reports()
            
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
            self._admin_name,
            self._on_logout,
            self._on_navigate,
            self._user_viewmodel,
            self._report_viewmodel
        )

    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)