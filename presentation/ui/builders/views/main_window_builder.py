from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from typing import Dict, Callable

from presentation.ui.factories import WidgetFactory, LayoutFactory


class MainWindowBuilder:
    def __init__(self, widget_factory: WidgetFactory, layout_factory: LayoutFactory, page_builders: Dict[str, Callable[[], QWidget]]):
        self.__wf = widget_factory
        self.__lf = layout_factory
        self.__page_builders = page_builders
        self.__stack = self.__wf.get("stacked").create()
        self.__window = QMainWindow()
        self.__page_indexes: Dict[str, int] = {}

    def build(self) -> QMainWindow:
        self.__window.setWindowTitle("Uamitos-CA")
        self.__window.setFixedSize(600, 200)

        for idx, (name, builder) in enumerate(self.__page_builders.items()):
            self.__page_indexes[name] = idx
            self.__stack.add_widget(builder().build())

        login_page = self.__page_indexes.get("login")
        self.__stack.set_current_index(login_page)

        self.__window.setCentralWidget(self.__stack.build())

        return self.__window
