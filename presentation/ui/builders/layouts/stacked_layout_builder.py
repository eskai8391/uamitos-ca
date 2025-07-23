from typing import Self, List

from PySide6.QtWidgets import QStackedLayout, QWidget
from .base_layout_builder import BaseLayoutBuilder

class StackedLayoutBuilder(BaseLayoutBuilder):
    def __init__(self, is_container: bool = False):
        super().__init__(is_container)
        self._widgets: list[QWidget] = []
        self._current_index: int = 0
        self._layout = QStackedLayout()

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
        self._apply_common()
        for w in self._widgets:
            self._layout.addWidget(w)
        self._layout.setCurrentIndex(self._current_index)
        return self._layout if self._container is None else self._container