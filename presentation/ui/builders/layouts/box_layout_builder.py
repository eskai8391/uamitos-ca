from typing import Self, AnyStr, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout
from .base_layout_builder import BaseLayoutBuilder

class BoxLayoutBuilder(BaseLayoutBuilder):
    def __init__(self, orientation: str = "h"):
        super().__init__()
        self._orientation = orientation
        self._layout = QVBoxLayout() if orientation == "v" else QHBoxLayout()
        self._widgets: list[tuple[QWidget,int, Qt.AlignmentFlag]] = []

    @property
    def orientation(self) -> AnyStr:
        return self._orientation

    @property
    def layout(self) -> QLayout:
        return self._layout

    @property
    def widgets(self) -> list[tuple[QWidget,int, Optional[Qt.AlignmentFlag]]]:
        return self._widgets

    def add_widget(self, widget: QWidget, stretch: int = 0, ) -> Self:
        self._widgets.append((widget, stretch, Qt.AlignmentFlag.AlignCenter))
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        self._layout.addLayout(layout, stretch)
        return self

    def build(self) -> QLayout:
        self._apply_common(self._layout, self._layout)
        for widget, stretch, alignment in self._widgets:
            self._layout.addWidget(widget, stretch, alignment)
        return self._layout
