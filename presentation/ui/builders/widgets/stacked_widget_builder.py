from typing import Self

from PySide6.QtWidgets import QStackedWidget, QWidget

from .base_widget_builder import BaseWidgetBuilder

class StackedWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QStackedWidget()

    def add_widget(self, widget: QWidget) -> Self:
        self._widget.addWidget(widget)
        return self

    def set_current_index(self, index: int) -> Self:
        self._widget.setCurrentIndex(index)
        return self