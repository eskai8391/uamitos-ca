from dependency_injector import containers, providers

from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.builders.views import MainWindowBuilder, LoginWidgetBuilder


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    widget_factory = providers.Singleton(WidgetFactory)
    layout_factory = providers.Singleton(LayoutFactory)

    # Builders for pages
    login_builder = providers.Factory(
        LoginWidgetBuilder,
        wf=widget_factory,
        lf=layout_factory
    )

    main_window_builder = providers.Factory(
        MainWindowBuilder,
        widget_factory=widget_factory,
        layout_factory=layout_factory,
        page_builders={'login': login_builder}
    )
