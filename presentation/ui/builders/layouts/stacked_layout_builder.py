from typing import Self, List

from PySide6.QtWidgets import QStackedLayout, QWidget
from .base_layout_builder import BaseLayoutBuilder

class StackedLayoutBuilder(BaseLayoutBuilder):
    def __init__(self):
        super().__init__()
        self._widgets: list[QWidget] = []
        self._current_index: int = 0

    @property
    def widgets(self) -> List[QWidget]:
        return self._widgets

    @property
    def current_index(self) -> int:
        return self._current_index

    def add_widget(self, widget: QWidget) -> Self:
        self._widgets.append(widget)
        return self

    def set_current_index(self, index: int) -> Self:
        self._current_index = index
        return self

    def build(self) -> QStackedLayout:
        layout = QStackedLayout()
        self._apply_common(layout, layout)
        for w in self._widgets:
            layout.addWidget(w)
        layout.setCurrentIndex(self._current_index)
        return layout
