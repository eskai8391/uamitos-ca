from dependency_injector import containers, providers

from application.app_coordinator import AppCoordinator
from presentation.controllers.auth_controller import AuthController
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.builders.views import MainWindowBuilder, LoginWindowBuilder


class AppContainer(containers.DeclarativeContainer):
    """Application dependency injection container"""
    
    config = providers.Configuration()
    
    # Controllers
    auth_controller = providers.Singleton(AuthController)
    
    # Factories
    widget_factory = providers.Singleton(WidgetFactory)
    layout_factory = providers.Singleton(LayoutFactory)
    
    # Coordinator (created after main window is built)
    coordinator = providers.Singleton(AppCoordinator)
    
    # Login page builder with auth controller
    login_builder = providers.Factory(
        LoginWindowBuilder,
        wf=widget_factory,
        lf=layout_factory,
        on_login_success=lambda uuid, role, name: coordinator().handle_login_success(uuid, role, name)
    )
    
    # Main window builder
    main_window_builder = providers.Factory(
        MainWindowBuilder,
        widget_factory=widget_factory,
        layout_factory=layout_factory,
        page_builders={'login': login_builder}
    )