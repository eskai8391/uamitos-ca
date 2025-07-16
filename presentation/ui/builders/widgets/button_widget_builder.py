from typing import Self, Callable

from PySide6.QtWidgets import QWidget, QPushButton

from .base_widget_builder import BaseWidgetBuilder

class ButtonWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self.__widget = QPushButton()

    def set_text(self, text: str) -> Self:
        self.__widget.setText(text)
        return self

    def build(self) -> QPushButton:
        self.__apply_common_properties(self.__widget)
        return self.__widget