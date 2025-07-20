from PySide6.QtWidgets import QLineEdit
from typing import Self
from .base_widget_builder import BaseWidgetBuilder

class LineEditWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QLineEdit()

    def set_placeholder(self, text: str) -> Self:
        self._widget.setPlaceholderText(text)
        return self

    def set_echo_mode(self, mode) -> Self:
        self._widget.setEchoMode(mode)
        return self