from typing import Self

from PySide6.QtWidgets import QLabel, QWidget
from dataclasses import dataclass

from .base_widget_builder import BaseWidgetBuilder

class LabelWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self.__widget = QLabel()

    def set_text(self, text) -> Self:
        """
        Set the text of the widget.
        :arg text: The text of the widget.
        """
        self.__widget.setText(text)
        return self

    def build(self) -> QLabel:
        self.__apply_common_properties(self.__widget)

        return self.__widget