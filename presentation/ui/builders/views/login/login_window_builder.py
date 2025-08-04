import copy
import os
from typing import Callable, Self, Optional

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QMessageBox, QLabel, QPushButton, QLayout, QHBoxLayout, QVBoxLayout
)

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.builders.directors.widget_director import WidgetDirector
from presentation.ui.builders.directors.layout_director import LayoutDirector
from presentation.ui.builders.utils.validation import validate_not_none, validate_type
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.viewmodels.login_viewmodel import LoginViewModel
from presentation.ui.widgets import CircularImageWidget


class LoginWindowBuilder(Builder):
    """
    Builder for creating login window widgets
    """
    def __init__(
        self,
        wf: WidgetFactory,
        lf: LayoutFactory,
        on_login_success: Callable[[str, str, str], None] = None
    ):
        """
        Initialize the login widget builder
        
        :param wf: Widget factory for creating widgets
        :param lf: Layout factory for creating layouts
        :param on_login_success: Callback for successful login (user_uuid, role, name)
        """
        validate_not_none(wf, "wf")
        validate_not_none(lf, "lf")
        validate_type(wf, "wf", WidgetFactory)
        validate_type(lf, "lf", LayoutFactory)
        
        self._wf = wf
        self._lf = lf
        self._on_login_success = on_login_success or (lambda u, r, n: None)

        # Create container widget that will hold everything
        self._container = QWidget()
        self._container.setObjectName("login-container")
        
        # Create view model
        self._view_model = LoginViewModel(self._container)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._style_path = os.path.join(current_dir, "login_styles.qss")

        self._create_layouts()
        self._create_form_components()
        self._assemble_components()

        self._connect_signals()
    
    def _create_layouts(self) -> None:
        """Create the main layout structure"""
        # Main container layout
        self._main_layout = (
            self._lf.get("vbox", is_container=True)
            .set_style_sheet(route=self._style_path)
            .set_alignment(Qt.AlignmentFlag.AlignCenter)
            .set_class("container")
        )

        self._welcome_layout = self._lf.get("vbox")
        self._form_layout = self._lf.get("form")
        self._error_layout = self._lf.get("vbox")
    
    def _create_form_components(self) -> None:
        """Create the form input components"""
        # Create header with director
        label_builder = self._wf.get("label").set_text("Bienvenido!")
        self._welcome_label = WidgetDirector.construct_from_preset(
            label_builder, 
            "header"
        )
        
        # Create user icon using UAMITOS logo
        self._user_icon = QLabel()
        self._user_icon.setObjectName("user-icon")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "assets", "window", "logoUamitos.png")
        self._user_icon.setPixmap(QPixmap(icon_path))
        self._user_icon.setScaledContents(True)
        self._user_icon.setFixedSize(150, 150)
        
        # Email input
        self._form_input_email = (
            self._wf.get("lineedit")
            .set_placeholder("Correo Electrónico")
            .set_object_name("email-input")
            .build()
        )
        
        # Password input
        self._form_input_password = (
            self._wf.get("lineedit")
            .set_placeholder("Contraseña")
            .set_echo_mode("Password")
            .set_object_name("password-input")
            .build()
        )
        
        # Create login button directly without using director
        self._form_button = (
            self._wf.get("button")
            .set_text("Iniciar sesión")
            .set_object_name("action_button")
            .set_default(True)
            .build()
        )
        
        # Error message label (hidden by default)
        self._error_label = (
            self._wf.get("label")
            .set_text("")
            .set_object_name("error-label")
            .set_alignment(Qt.AlignmentFlag.AlignCenter)
            .build()
        )
        self._error_label.setVisible(False)
    
    def _assemble_components(self) -> None:
        """Assemble all components into their layouts"""
        # Create a container for user icon
        icon_container = QWidget()
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.addStretch(1)
        icon_layout.addWidget(self._user_icon)
        icon_layout.addStretch(1)
        
        # Add user icon and welcome label to welcome layout
        self._welcome_layout.add_widget(icon_container)
        self._welcome_layout.add_widget(self._welcome_label)
        
        # Add error message to error layout
        self._error_layout.add_widget(self._error_label)
        
        # Assemble form with inputs
        (self._form_layout
            .add_row("", self._form_input_email)
            .add_row("", self._form_input_password)
            .add_row("", self._form_button)
        )
        
        # Add sub-layouts to main layout
        self._main_layout.add_layout(self._welcome_layout.build(), 1)
        self._main_layout.add_layout(self._error_layout.build())
        self._main_layout.add_layout(self._form_layout.build(), 1)
    
    def _connect_signals(self) -> None:
        """Connect UI events to view model"""
        # Connect signals from view model
        self._view_model.loginSuccessful.connect(self._handle_login_success)
        self._view_model.loginFailed.connect(self._handle_login_error)
        
        # Connect input fields to view model
        self._form_input_email.textChanged.connect(self._update_email)
        self._form_input_password.textChanged.connect(self._update_password)
        
        # Connect button to login action
        self._form_button.clicked.connect(self._view_model.login)
        self._form_button.clicked.connect(lambda _: print("Login button clicked"))
        
        # Connect Enter key press in password field to login action
        self._form_input_password.returnPressed.connect(self._view_model.login)
        
        # Debug message for connection verification
        print("Login form connections established")

    @Slot(str)
    def _update_email(self, text: str) -> None:
        """Update the email in the view model"""
        print(f"Email changed to: {text}")
        self._view_model.email = text
        
    def _update_password(self, text: str) -> None:
        """Update the password in the view model"""
        self._view_model.password = text
    
    def _handle_login_success(self, user_uuid: str, role: str, name: str) -> None:
        """Handle successful login"""
        # Clear error message
        self._error_label.setText("")
        self._error_label.setVisible(False)
        
        # Call the callback
        if self._on_login_success:
            self._on_login_success(user_uuid, role, name)
        
        # Clear inputs
        self._view_model.clear_inputs()
        self._form_input_email.clear()
        self._form_input_password.clear()
    
    def _handle_login_error(self, error_message: str) -> None:
        """Handle login error"""
        # Show error message
        self._error_label.setText(error_message)
        self._error_label.setVisible(True)
        
        # Clear password
        self._form_input_password.clear()
        self._view_model.password = ""
    
    def create(self) -> Self:
        """
        Creates a new instance of the login widget builder
        
        :return: A new builder instance
        """
        return type(self)(self._wf, self._lf, self._on_login_success)
    
    def clone(self) -> Self:
        """
        Creates a deep copy of the builder
        
        :return: A cloned builder instance
        """
        return copy.deepcopy(self)
    
    def build(self) -> QWidget:
        """
        Builds the login widget
        
        :return: The built login widget
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
    
    def set_on_login_success(self, callback: Callable[[str, str, str], None]) -> Self:
        """
        Sets the callback for successful login
        
        :param callback: Function to call on successful login (user_uuid, role, name)
        :return: Self for method chaining
        """
        validate_not_none(callback, "callback")
        self._on_login_success = callback
        return self
    
    def get_email_input(self) -> QLineEdit:
        """
        Gets the email input widget
        
        :return: Email input widget
        """
        return self._form_input_email
    
    def get_password_input(self) -> QLineEdit:
        """
        Gets the password input widget
        
        :return: Password input widget
        """
        return self._form_input_password