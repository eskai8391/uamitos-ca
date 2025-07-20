from PySide6.QtWidgets import QComboBox
from typing import Self, Iterable
from .base_widget_builder import BaseWidgetBuilder

class ComboBoxWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QComboBox()

    def add_items(self, items: Iterable[str]) -> Self:
        self._widget.addItems(list(items))
        return self

    def set_current_index(self, index: int) -> Self:
        self._widget.setCurrentIndex(index)
        return self