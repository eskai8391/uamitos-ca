from typing import Self
from PySide6.QtWidgets import QPushButton

from .base_widget_builder import BaseWidgetBuilder

class ButtonWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QPushButton()

    def set_text(self, text: str) -> Self:
        self._widget.setText(text)
        return self

    def set_default(self, default:bool) -> Self:
        self._widget.setAutoDefault(default)
        return self