from PySide6.QtWidgets import QCheckBox
from typing import Self
from .base_widget_builder import BaseWidgetBuilder

class CheckBoxWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QCheckBox()

    def set_checked(self, state: bool = True) -> Self:
        self._widget.setChecked(state)
        return self

    def set_text(self, text: str) -> Self:
        self._widget.setText(text)
        return self