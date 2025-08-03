from dependency_injector import containers, providers

from application.app_coordinator import AppCoordinator
from presentation.controllers.auth_controller import AuthController
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.builders.views import MainWindowBuilder, LoginWindowBuilder
from infrastructure.api_client import ApiClient, StudentApiClient, TeacherApiClient, EventApiClient
from presentation.ui.viewmodels import LoginViewModel, StudentViewModel, TeacherViewModel, EventViewModel


class AppContainer(containers.DeclarativeContainer):
    """Application dependency injection container"""
    
    config = providers.Configuration()
    
    # Create API client as a Singleton for token consistency
    # This ensures the same API client instance is used throughout the app
    api_client = providers.Singleton(ApiClient)
    
    # Controllers
    auth_controller = providers.Singleton(AuthController, api_client=api_client)
    
    # Factories
    widget_factory = providers.Singleton(WidgetFactory)
    layout_factory = providers.Singleton(LayoutFactory)
    
    # Always use the same api_client instance for consistent token handling
    # Using providers.Factory ensures we get fresh instances but sharing the same api_client
    student_api_client = providers.Factory(StudentApiClient, api_client=api_client)
    teacher_api_client = providers.Factory(TeacherApiClient, api_client=api_client)
    event_api_client = providers.Factory(EventApiClient, api_client=api_client)
    
    # ViewModels
    student_viewmodel = providers.Singleton(StudentViewModel, student_api_client=student_api_client)
    teacher_viewmodel = providers.Singleton(TeacherViewModel, teacher_api_client=teacher_api_client)
    event_viewmodel = providers.Singleton(EventViewModel, event_api_client=event_api_client)
    
    # Coordinator (created after main window is built)
    coordinator = providers.Singleton(AppCoordinator)
    
    # Login page builder with auth controller - instantiated as a singleton
    login_builder = providers.Singleton(
        LoginWindowBuilder,
        wf=widget_factory,
        lf=layout_factory,
        # Use wired_coordinator to avoid circular reference
        on_login_success=lambda uuid, role, name: None
    )
    
    # Main window builder
    main_window_builder = providers.Factory(
        MainWindowBuilder,
        widget_factory=widget_factory,
        layout_factory=layout_factory,
        page_builders={'login': login_builder}
    )