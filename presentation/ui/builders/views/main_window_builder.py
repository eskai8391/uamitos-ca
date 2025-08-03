from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from typing import Dict, Callable, Any, Union

from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.builders.builder_interface import Builder


class MainWindowBuilder:
    def __init__(
            self,
            widget_factory: WidgetFactory,
            layout_factory: LayoutFactory,
            page_builders: Dict[str, Any]  # Allow Factory or Builder
    ):
        self.__wf = widget_factory
        self.__lf = layout_factory
        self.__page_builders = page_builders
        self.__stack = self.__wf.get("stacked").create()
        self.__window = QMainWindow()
        self.__page_indexes: Dict[str, int] = {}

    def build(self) -> QMainWindow:
        self.__window.setWindowTitle("Uamitos-CA")
        self.__window.setFixedSize(500, 580)

        for idx, (name, builder_or_factory) in enumerate(self.__page_builders.items()):
            self.__page_indexes[name] = idx
            # Check if it's a Factory provider that needs to be called first
            if hasattr(builder_or_factory, '__call__') and not hasattr(builder_or_factory, 'build'):
                builder = builder_or_factory()
            else:
                builder = builder_or_factory
            
            # Now call build() on the actual builder instance
            self.__stack.add_widget(builder.build())

        login_page = self.__page_indexes.get("login")
        self.__stack.set_current_index(login_page)

        self.__window.setCentralWidget(self.__stack.build())

        return self.__window
