from typing import Self

from PySide6.QtWidgets import QGridLayout, QWidget
from .base_layout_builder import BaseLayoutBuilder

class GridLayoutBuilder(BaseLayoutBuilder):
    def __init__(self, is_container: bool = False):
        super().__init__(is_container)
        self._cells: list[tuple[QWidget,int,int,int,int, int]] = []
        self._layout = QGridLayout()

    @property
    def cells(self) -> list[tuple[QWidget,int,int,int,int, int]]:
        return self._cells

    def add_widget(
        self,
        widget: QWidget,
        row: int,
        col: int,
        rowspan: int = 1,
        colspan: int = 1,
        stretch: int = 0
    ) -> Self:
        self._cells.append((widget, row, col, rowspan, colspan, stretch))
        return self

    def build(self) -> QGridLayout:
        self._apply_common()
        for widget, r, c, rs, cs, st in self._cells:
            self._layout.addWidget(widget, r, c, rs, cs)
            if st:
                self._layout.setRowStretch(r, st)
                self._layout.setColumnStretch(c, st)
        return self._layout if self._container is None else self._container