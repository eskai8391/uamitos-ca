from typing import Self

from PySide6.QtWidgets import QLabel, QWidget
from dataclasses import dataclass

from .base_widget_builder import BaseWidgetBuilder

class LabelWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QLabel()

    def set_text(self, text) -> Self:
        """
        Set the text of the label.
        :arg text: The text of the label.
        """
        self._widget.setText(text)
        return self