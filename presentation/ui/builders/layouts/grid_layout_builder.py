from typing import Self

from PySide6.QtWidgets import QGridLayout, QWidget
from .base_layout_builder import BaseLayoutBuilder

class GridLayoutBuilder(BaseLayoutBuilder):
    def __init__(self):
        super().__init__()
        self._cells: list[tuple[QWidget,int,int,int,int, int]] = []

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
        layout = QGridLayout()
        self._apply_common(layout, layout.parentWidget() or layout)
        for widget, r, c, rs, cs, st in self._cells:
            layout.addWidget(widget, r, c, rs, cs)
            if st:
                layout.setRowStretch(r, st)
                layout.setColumnStretch(c, st)
        return layout
