from typing import Self, AnyStr, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout
from .base_layout_builder import BaseLayoutBuilder

class BoxLayoutBuilder(BaseLayoutBuilder):
    def __init__(self, *, is_container: bool = False, orientation: str = "h"):
        super().__init__(is_container)
        self._orientation = orientation
        self._layout = QVBoxLayout() if orientation == "v" else QHBoxLayout()
        self._widgets: list[tuple[QWidget, int, Qt.AlignmentFlag]] = []

    @property
    def orientation(self) -> AnyStr:
        return self._orientation

    @property
    def layout(self) -> QLayout:
        return self._layout

    @property
    def widgets(self) -> list[tuple[QWidget, int, Qt.AlignmentFlag]]:
        return self._widgets

    def add_widget(self, widget: QWidget, **kwargs) -> Self:
        stretch = kwargs.get('stretch', 0)
        alignment = kwargs.get('alignment', "center")

        if isinstance(alignment, str):
            match alignment.lower():
                # Alineaciones horizontales
                case "left":
                    alignment = Qt.AlignmentFlag.AlignLeft
                case "right":
                    alignment = Qt.AlignmentFlag.AlignRight
                case "hcenter":
                    alignment = Qt.AlignmentFlag.AlignHCenter
                case "justify":
                    alignment = Qt.AlignmentFlag.AlignJustify
                
                # Alineaciones verticales
                case "top":
                    alignment = Qt.AlignmentFlag.AlignTop
                case "bottom":
                    alignment = Qt.AlignmentFlag.AlignBottom
                case "vcenter":
                    alignment = Qt.AlignmentFlag.AlignVCenter
                case "baseline":
                    alignment = Qt.AlignmentFlag.AlignBaseline
                
                # Combinaciones comunes
                case "center":
                    alignment = Qt.AlignmentFlag.AlignCenter  # AlignVCenter | AlignHCenter
                case "topleft":
                    alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
                case "topright":
                    alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
                case "bottomleft":
                    alignment = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
                case "bottomright":
                    alignment = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
                
                # Default
                case _:
                    alignment = Qt.AlignmentFlag.AlignCenter
        
        # Agregar el widget con sus propiedades
        self._widgets.append((widget, stretch, alignment))
        return self

    def add_layout(self, layout: QLayout, stretch: int = 0) -> Self:
        self._layout.addLayout(layout, stretch)
        return self

    def add_stretch(self) -> Self:
        self._layout.addStretch()
        return self

    def build(self) -> QVBoxLayout | QHBoxLayout | QWidget:
        self._apply_common()
        for widget, stretch, alignment in self._widgets:
            self._layout.addWidget(widget, stretch, alignment)
        return self._layout if self._container is None else self._container