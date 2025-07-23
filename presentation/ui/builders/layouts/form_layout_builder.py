from typing import Self

from PySide6.QtWidgets import QFormLayout, QWidget
from .base_layout_builder import BaseLayoutBuilder

class FormLayoutBuilder(BaseLayoutBuilder):
    def __init__(self, is_container: bool = False):
        super().__init__(is_container)
        self._layout = QFormLayout()
        self._rows: list[tuple[str, QWidget]] = []

    @property
    def rows(self) -> list[tuple[str, QWidget]]:
        return self._rows

    def add_row(self, label: str, widget: QWidget) -> Self:
        self._rows.append((label, widget))
        return self

    def add_widget(self, widget: QWidget) -> Self:
        pass

    def build(self) -> QFormLayout:
        self._apply_common()
        for lab, wid in self._rows:
            self._layout.addRow(lab, wid)
        return self._layout if self._container is None else self._container