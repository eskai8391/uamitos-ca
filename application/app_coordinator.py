import logging
from typing import Optional, Dict, Any, TYPE_CHECKING

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout

from domain.entities.user import UserRole
from presentation.ui.builders.views.dashboard.dashboard_window_builder import DashboardWindowBuilder

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from application.container import AppContainer
from presentation.ui.builders.views.dashboard.teacher_dashboard_builder import TeacherDashboardBuilder
from presentation.ui.builders.views.dashboard.student_details_builder import StudentDetailsBuilder
from presentation.ui.builders.views.dashboard.teacher_details_builder import TeacherDetailsBuilder
from presentation.ui.builders.views.dashboard.events_details_builder import EventsDetailsBuilder
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
        
        # Dashboard content stack
        self._dashboard_stack: Optional[QStackedWidget] = None
        self._dashboard_views: Dict[str, QWidget] = {}
        self._dashboard_builder = None
        self._current_detail_view = None
        self._dashboard_container = None
        
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
            
            dashboard = None
            
            # Create appropriate dashboard based on role
            if user_role == UserRole.TEACHER:
                # Create teacher dashboard
                self._logger.info(f"Creating teacher dashboard for {full_name}")
                # Get container instance and view models
                from application.container import AppContainer
                import logging
                
                # Set up logger for debugging token issues
                debug_logger = logging.getLogger("app_coordinator.dashboard")
                
                # Get the shared container instance
                container = AppContainer()
                
                # Debug log all container objects for token verification
                api_client = container.api_client()
                auth_controller = container.auth_controller()
                student_api = container.student_api_client()
                teacher_api = container.teacher_api_client()
                
                debug_logger.info(f"Token check - Main API client: {id(api_client)}, has token: {bool(api_client._token)}")
                debug_logger.info(f"Token check - Auth controller API: {id(auth_controller._api_client)}, shared: {auth_controller._api_client is api_client}")
                debug_logger.info(f"Token check - StudentApiClient base API: {id(student_api._api_client)}, shared: {student_api._api_client is api_client}")
                debug_logger.info(f"Token check - TeacherApiClient base API: {id(teacher_api._api_client)}, shared: {teacher_api._api_client is api_client}")
                
                # Always explicitly set the token on all API clients to ensure consistency
                if hasattr(auth_controller, '_current_user') and auth_controller._current_user:
                    token = auth_controller._current_user.token
                    debug_logger.info(f"Setting token from auth_controller to all API clients: {token[:10]}...")
                    # Set token on all API client instances to ensure consistency
                    api_client.set_token(token)
                    student_api._api_client.set_token(token)
                    teacher_api._api_client.set_token(token)
                
                teacher_dashboard_builder = TeacherDashboardBuilder(
                    wf=self._widget_factory,
                    lf=self._layout_factory,
                    teacher_name=full_name,
                    on_logout=self.handle_logout,
                    on_navigate=self.handle_dashboard_navigation,
                    student_viewmodel=container.student_viewmodel(),
                    teacher_viewmodel=container.teacher_viewmodel(),
                    event_viewmodel=container.event_viewmodel()
                )
                
                # Set builder for future reference
                self._last_dashboard_builder = teacher_dashboard_builder
                self._dashboard_builder = teacher_dashboard_builder
                
                # We've already set the logout handler in constructor
                
                # Create main dashboard
                teacher_dashboard = teacher_dashboard_builder.build()
                
                # Create container for dashboard and detail views
                self._dashboard_container = QWidget()
                container_layout = QVBoxLayout()
                self._dashboard_container.setLayout(container_layout)
                
                # Create stack for main dashboard and detail views
                self._dashboard_stack = QStackedWidget()
                container_layout.addWidget(self._dashboard_stack)
                container_layout.setContentsMargins(0, 0, 0, 0)
                
                # Add teacher dashboard as the first view
                self._dashboard_stack.addWidget(teacher_dashboard)
                self._dashboard_views["main"] = teacher_dashboard
                
                # Use container as the dashboard
                dashboard = self._dashboard_container
            else:
                # Create default dashboard for other roles
                self._logger.info(f"Creating standard dashboard for {full_name} with role {role}")
                dashboard_builder = DashboardWindowBuilder(
                    wf=self._widget_factory,
                    lf=self._layout_factory,
                    user_role=user_role,
                    user_name=full_name,
                    on_logout=self.handle_logout
                )
                
                dashboard = dashboard_builder.build()
            
            # Add to stacked widget and register page
            index = self._stacked_widget.addWidget(dashboard)
            self.register_page("dashboard", index)
            
            # Navigate to dashboard
            self.navigate_to("dashboard")
            
            # Update window size for dashboard
            self._main_window.setFixedSize(1100, 750)
            
        except Exception as e:
            self._logger.error(f"Error creating dashboard: {e}", exc_info=True)
    
    def handle_logout(self) -> None:
        """
        Handle logout action
        """
        self._logger.info("Logging out")
        
        # Clear current user
        self._current_user = {}
        
        # Clear dashboard references
        self._dashboard_builder = None
        self._dashboard_stack = None
        self._dashboard_views = {}
        self._current_detail_view = None
        self._dashboard_container = None
        
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
    
    def _show_student_details(self, student_name: str) -> None:
        """
        Show student details view
        
        :param student_name: Name of the student to show details for
        """
        self._logger.info(f"Showing details for student: {student_name}")
        
        if not self._dashboard_stack:
            self._logger.warning("Dashboard stack not initialized")
            return
            
        # Create student details view if it doesn't exist
        view_key = f"student_{student_name}"
        
        if view_key not in self._dashboard_views:
            # Create student details view
            student_details_builder = StudentDetailsBuilder(
                wf=self._widget_factory,
                lf=self._layout_factory,
                student_name=student_name,
                on_back=lambda: self._back_to_main_dashboard()
            )
            
            student_details_view = student_details_builder.build()
            self._dashboard_stack.addWidget(student_details_view)
            self._dashboard_views[view_key] = student_details_view
        
        # Show the details view
        self._dashboard_stack.setCurrentWidget(self._dashboard_views[view_key])
        self._current_detail_view = view_key
    
    def _show_teacher_details(self, teacher_name: str) -> None:
        """
        Show teacher details view
        
        :param teacher_name: Name of the teacher to show details for
        """
        self._logger.info(f"Showing details for teacher: {teacher_name}")
        
        if not self._dashboard_stack:
            self._logger.warning("Dashboard stack not initialized")
            return
            
        # Create teacher details view if it doesn't exist
        view_key = f"teacher_{teacher_name}"
        
        if view_key not in self._dashboard_views:
            # Create teacher details view
            teacher_details_builder = TeacherDetailsBuilder(
                wf=self._widget_factory,
                lf=self._layout_factory,
                teacher_name=teacher_name,
                on_back=lambda: self._back_to_main_dashboard()
            )
            
            teacher_details_view = teacher_details_builder.build()
            self._dashboard_stack.addWidget(teacher_details_view)
            self._dashboard_views[view_key] = teacher_details_view
        
        # Show the details view
        self._dashboard_stack.setCurrentWidget(self._dashboard_views[view_key])
        self._current_detail_view = view_key
    
    def _show_teacher_list_view(self) -> None:
        """
        Show teacher list view with all teachers
        """
        self._logger.info("Showing teacher list view")
        
        # For demonstration purposes, show details for a specific teacher
        # For safety, check if we have a teacher with this name in our dashboard
        try:
            # Show the first teacher by default
            self._show_teacher_details("Laura Gómez")
        except Exception as e:
            self._logger.error(f"Error showing teacher details: {e}")
            # Fall back to main dashboard
            if self._dashboard_stack and "main" in self._dashboard_views:
                self._dashboard_stack.setCurrentWidget(self._dashboard_views["main"])
    
    def _show_events_view(self) -> None:
        """
        Show events calendar and list
        """
        self._logger.info("Showing events view")
        
        if not self._dashboard_stack:
            self._logger.warning("Dashboard stack not initialized")
            return
            
        # Create events view if it doesn't exist
        view_key = "events"
        
        if view_key not in self._dashboard_views:
            # Create events view
            events_builder = EventsDetailsBuilder(
                wf=self._widget_factory,
                lf=self._layout_factory,
                on_back=lambda: self._back_to_main_dashboard()
            )
            
            events_view = events_builder.build()
            self._dashboard_stack.addWidget(events_view)
            self._dashboard_views[view_key] = events_view
        
        # Show the events view
        self._dashboard_stack.setCurrentWidget(self._dashboard_views[view_key])
        self._current_detail_view = view_key
    
    def _back_to_main_dashboard(self) -> None:
        """
        Return to the main dashboard from a detail view
        """
        self._logger.info("Returning to main dashboard")
        
        if not self._dashboard_stack or "main" not in self._dashboard_views:
            self._logger.warning("Cannot return to main dashboard - not initialized")
            return
            
        # Show main dashboard
        self._dashboard_stack.setCurrentWidget(self._dashboard_views["main"])
        self._current_detail_view = None
    
    def handle_dashboard_navigation(self, section: str) -> None:
        """
        Handle navigation within the dashboard
        
        :param section: Section to navigate to
        """
        self._logger.info(f"Dashboard navigation to section: {section}")
        
        # Check if it's a special format for details views
        if ":" in section:
            action, param = section.split(":", 1)
            
            if action == "student_details":
                self._show_student_details(param)
                return
                
            elif action == "teacher_details":
                self._show_teacher_details(param)
                return
        
        # Return to main dashboard view for standard sections
        if self._dashboard_stack and "main" in self._dashboard_views:
            self._dashboard_stack.setCurrentWidget(self._dashboard_views["main"])
            
        # Handle different sections
        if section == "inicio":
            self._logger.info("Navigating to home section")
            # Show main dashboard
            
        elif section == "estudiantes":
            self._logger.info("Navigating to students section")
            # You could show a student list view here
            
        elif section == "profesores":
            self._logger.info("Navigating to teachers section")
            self._show_teacher_list_view()
            
        elif section == "eventos":
            self._logger.info("Navigating to events section")
            self._show_events_view()
            
        elif section == "configuracion":
            self._logger.info("Navigating to settings section")
            # Not implemented yet