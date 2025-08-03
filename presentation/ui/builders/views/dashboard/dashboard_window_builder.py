import os
from typing import Callable, Self, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLayout

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from domain.entities.user import UserRole


class DashboardWindowBuilder(Builder):
    """
    Builder for creating dashboard window
    """
    def __init__(
        self,
        wf: WidgetFactory,
        lf: LayoutFactory,
        user_role: UserRole,
        user_name: str,
        on_logout: Callable[[], None] = None,
        on_navigation: Dict[str, Callable[[], None]] = None
    ):
        """
        Initialize the dashboard widget builder
        
        :param wf: Widget factory
        :param lf: Layout factory
        :param user_role: User role to determine dashboard content
        :param user_name: User name to display
        :param on_logout: Callback for logout action
        :param on_navigation: Callbacks for navigation actions
        """
        self._wf = wf
        self._lf = lf
        self._user_role = user_role
        self._user_name = user_name
        self._on_logout = on_logout or (lambda: None)
        self._on_navigation = on_navigation or {}
        
        # Create container widget that will hold everything
        self._container = QWidget()
        self._container.setObjectName("dashboard-container")
        
        # Get style sheet path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._style_path = os.path.join(current_dir, "dashboard_styles.qss")
        print(f"Dashboard style path: {self._style_path}")
        
        # Verify if file exists
        if not os.path.exists(self._style_path):
            print(f"WARNING: Dashboard style file not found at {self._style_path}")
            # Look for the file in parent directories
            parent_dir = os.path.dirname(current_dir)
            alt_path = os.path.join(parent_dir, "dashboard_styles.qss")
            if os.path.exists(alt_path):
                print(f"Found style file at alternative location: {alt_path}")
                self._style_path = alt_path
        
        # Create components
        self._create_layouts()
        self._create_header()
        self._create_sidebar()
        self._create_content_area()
        self._assemble_components()
    
    def _create_layouts(self) -> None:
        """Create the main layout structure"""
        # Main container layout
        self._main_layout = (
            self._lf.get("vbox", is_container=True)
            .set_style_sheet(route=self._style_path)
            .set_class("dashboard-container")
        )
        
        # Header layout
        self._header_layout = self._lf.get("hbox")
        
        # Content layout - horizontal box that contains sidebar and main content
        self._content_layout = self._lf.get("hbox")
        
        # Sidebar layout
        self._sidebar_layout = self._lf.get("vbox")
        
        # Main content area layout
        self._main_content_layout = self._lf.get("stacked")
    
    def _create_header(self) -> None:
        """Create the header components"""
        # App title
        self._app_title = (
            self._wf.get("label")
            .set_text("Uamitos-CA")
            .set_font_size(18)
            .set_font_bold(True)
            .set_object_name("app-title")
            .build()
        )
        
        # User info
        self._user_info = (
            self._wf.get("label")
            .set_text(f"Bienvenido, {self._user_name}")
            .set_font_size(12)
            .set_alignment(Qt.AlignmentFlag.AlignRight)
            .set_object_name("user-info")
            .build()
        )
        
        # Logout button
        self._logout_button = (
            self._wf.get("button")
            .set_text("Cerrar sesión")
            .set_object_name("logout-button")
            .build()
        )
        
        # Connect logout action
        self._logout_button.clicked.connect(self._on_logout)
    
    def _create_sidebar(self) -> None:
        """Create sidebar with navigation options based on user role"""
        self._nav_buttons = {}
        
        # Common options for all roles
        self._nav_buttons["dashboard"] = self._create_nav_button("Dashboard", "dashboard")
        self._nav_buttons["profile"] = self._create_nav_button("Mi Perfil", "profile")
        
        # Role-specific options
        if self._user_role == UserRole.ADMIN:
            self._nav_buttons["users"] = self._create_nav_button("Usuarios", "users")
            self._nav_buttons["subjects"] = self._create_nav_button("Materias", "subjects")
            self._nav_buttons["reports"] = self._create_nav_button("Reportes", "reports")
        
        elif self._user_role == UserRole.TEACHER:
            self._nav_buttons["subjects"] = self._create_nav_button("Mis Materias", "subjects")
            self._nav_buttons["attendance"] = self._create_nav_button("Asistencia", "attendance")
            self._nav_buttons["grades"] = self._create_nav_button("Calificaciones", "grades")
            self._nav_buttons["reports"] = self._create_nav_button("Reportes", "reports")
        
        elif self._user_role == UserRole.STUDENT:
            self._nav_buttons["schedule"] = self._create_nav_button("Horario", "schedule")
            self._nav_buttons["grades"] = self._create_nav_button("Calificaciones", "grades")
            self._nav_buttons["attendance"] = self._create_nav_button("Asistencia", "attendance")
    
    def _create_nav_button(self, label: str, action: str) -> QPushButton:
        """Create a navigation button with the given label and action"""
        button = (
            self._wf.get("button")
            .set_text(label)
            .set_object_name("nav-button")
            .build()
        )
        
        # Connect action if provided
        if action in self._on_navigation:
            button.clicked.connect(self._on_navigation[action])
        
        return button
    
    def _create_content_area(self) -> None:
        """Create the main content area placeholder"""
        self._placeholder = (
            self._wf.get("label")
            .set_text("Selecciona una opción del menú")
            .set_alignment(Qt.AlignmentFlag.AlignCenter)
            .set_font_size(16)
            .set_object_name("placeholder")
            .build()
        )
    
    def _assemble_components(self) -> None:
        """Assemble all components into their layouts"""
        # Assemble header
        self._header_layout.add_widget(self._app_title, stretch=2)
        self._header_layout.add_widget(self._user_info, stretch=1)
        self._header_layout.add_widget(self._logout_button)
        
        # Assemble sidebar
        for button in self._nav_buttons.values():
            self._sidebar_layout.add_widget(button)
        
        # Add placeholder to main content area
        self._main_content_layout.add_widget(self._placeholder)
        
        # Assemble content layout
        self._content_layout.add_layout(self._sidebar_layout.build(), stretch=1)
        self._content_layout.add_layout(self._main_content_layout.build(), stretch=4)
        
        # Assemble main layout
        self._main_layout.add_layout(self._header_layout.build())
        self._main_layout.add_layout(self._content_layout.build(), stretch=1)
    
    def create(self) -> Self:
        """
        Creates a new instance of the dashboard window builder
        
        :return: A new builder instance
        """
        return type(self)(
            self._wf, 
            self._lf, 
            self._user_role, 
            self._user_name, 
            self._on_logout, 
            self._on_navigation
        )
    
    def clone(self) -> Self:
        """
        Creates a deep copy of the builder
        
        :return: A cloned builder instance
        """
        import copy
        return copy.deepcopy(self)
    
    def build(self) -> QWidget:
        """
        Builds the dashboard widget
        
        :return: The built dashboard widget
        """
        # Get the layout from the layout builder
        main_layout = self._main_layout.build()
        
        # Check if we got a QLayout (normal case) or a QWidget (container case)
        if isinstance(main_layout, QLayout):
            # Apply the layout to the container widget
            self._container.setLayout(main_layout)
        else:
            # We got a container widget with layout already applied
            # Copy its layout to our container
            if main_layout.layout():
                self._container.setLayout(main_layout.layout())
            
            # Apply any styling from the layout builder container
            if main_layout.styleSheet():
                self._container.setStyleSheet(main_layout.styleSheet())
        
        return self._container
    
    def add_page(self, name: str, widget: QWidget) -> Self:
        """
        Adds a page to the main content area
        
        :param name: Name of the page
        :param widget: Widget to add
        :return: Self for method chaining
        """
        self._main_content_layout.add_widget(widget)
        return self
    
    def set_on_logout(self, callback: Callable[[], None]) -> Self:
        """
        Sets the callback for logout action
        
        :param callback: Function to call on logout
        :return: Self for method chaining
        """
        self._on_logout = callback
        if hasattr(self, "_logout_button"):
            self._logout_button.clicked.disconnect()
            self._logout_button.clicked.connect(callback)
        return self
    
    def set_on_navigation(self, action: str, callback: Callable[[], None]) -> Self:
        """
        Sets the callback for a navigation action
        
        :param action: Action name
        :param callback: Function to call on navigation
        :return: Self for method chaining
        """
        self._on_navigation[action] = callback
        if action in self._nav_buttons:
            button = self._nav_buttons[action]
            for handler in button.clicked.disconnect():
                pass
            button.clicked.connect(callback)
        return self