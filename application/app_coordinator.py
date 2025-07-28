import logging
from typing import Optional, Dict, Any

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget

from domain.entities.user import UserRole
from presentation.ui.builders.views.dashboard.dashboard_window_builder import DashboardWindowBuilder
from presentation.ui.factories import WidgetFactory, LayoutFactory


class AppCoordinator:
    """
    Coordinator that manages application flow and navigation between screens
    """
    
    def __init__(self, main_window: QMainWindow, stacked_widget: QStackedWidget):
        self._logger = logging.getLogger(__name__)
        self._main_window = main_window
        self._stacked_widget = stacked_widget
        self._current_user: Dict[str, Any] = {}
        
        # UI factories
        self._widget_factory = WidgetFactory()
        self._layout_factory = LayoutFactory()
        
        # Page indexes
        self._page_indexes: Dict[str, int] = {}
        
    def register_page(self, name: str, index: int) -> None:
        """
        Register a page with a name and index
        
        :param name: Name of the page
        :param index: Index in the stacked widget
        """
        self._page_indexes[name] = index
        self._logger.info(f"Registered page '{name}' at index {index}")
    
    def navigate_to(self, page_name: str) -> bool:
        """
        Navigate to a page by name
        
        :param page_name: Name of the page to navigate to
        :return: True if navigation was successful, False otherwise
        """
        if page_name in self._page_indexes:
            index = self._page_indexes[page_name]
            self._stacked_widget.setCurrentIndex(index)
            self._logger.info(f"Navigated to page '{page_name}'")
            return True
        else:
            self._logger.warning(f"Page '{page_name}' not found")
            return False
    
    def handle_login_success(self, user_uuid: str, role: str, full_name: str) -> None:
        """
        Handle successful login by creating and showing the appropriate dashboard
        
        :param user_uuid: User UUID
        :param role: User role (admin, teacher, student)
        :param full_name: User full name
        """
        self._logger.info(f"Login successful for user {user_uuid} with role {role}")
        
        # Store current user info
        self._current_user = {
            "uuid": user_uuid,
            "role": role,
            "full_name": full_name
        }
        
        # Create dashboard based on role
        try:
            # Determine user role
            user_role = UserRole(role)
            
            # Create dashboard builder
            dashboard_builder = DashboardWindowBuilder(
                wf=self._widget_factory,
                lf=self._layout_factory,
                user_role=user_role,
                user_name=full_name,
                on_logout=self.handle_logout
            )
            
            # Build dashboard
            dashboard = dashboard_builder.build()
            
            # Add to stacked widget and register page
            index = self._stacked_widget.addWidget(dashboard)
            self.register_page("dashboard", index)
            
            # Navigate to dashboard
            self.navigate_to("dashboard")
            
            # Update window size for dashboard
            self._main_window.setFixedSize(900, 700)
            
        except Exception as e:
            self._logger.error(f"Error creating dashboard: {e}", exc_info=True)
    
    def handle_logout(self) -> None:
        """
        Handle logout action
        """
        self._logger.info("Logging out")
        
        # Clear current user
        self._current_user = {}
        
        # Navigate back to login page
        if self.navigate_to("login"):
            # Reset window size for login
            self._main_window.setFixedSize(500, 580)
            
            # Remove dashboard from stacked widget if it exists
            if "dashboard" in self._page_indexes:
                index = self._page_indexes["dashboard"]
                widget = self._stacked_widget.widget(index)
                if widget:
                    self._stacked_widget.removeWidget(widget)
                del self._page_indexes["dashboard"]