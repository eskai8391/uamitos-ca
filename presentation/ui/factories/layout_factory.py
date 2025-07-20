from typing import Literal, Type
from presentation.ui.builders.layouts.base_layout_builder import BaseLayoutBuilder
from presentation.ui.builders.layouts.box_layout_builder import BoxLayoutBuilder
from presentation.ui.builders.layouts.form_layout_builder import FormLayoutBuilder
from presentation.ui.builders.layouts.grid_layout_builder import GridLayoutBuilder
from presentation.ui.builders.layouts.stacked_layout_builder import StackedLayoutBuilder

LayoutType = Literal["hbox", "vbox", "form", "grid", "stacked"]

class LayoutFactory:
    def __init__(self):
        self._map: dict[LayoutType, Type[BaseLayoutBuilder]] = {
            "hbox":    lambda: BoxLayoutBuilder("h"),
            "vbox":    lambda: BoxLayoutBuilder("v"),
            "form":    FormLayoutBuilder,
            "grid":    GridLayoutBuilder,
            "stacked": StackedLayoutBuilder,
        }

    def get(self, kind: LayoutType) -> BaseLayoutBuilder:
        try:
            factory = self._map[kind]
        except KeyError:
            raise ValueError(f"Layout '{kind}' no soportado")
        return factory().create()
