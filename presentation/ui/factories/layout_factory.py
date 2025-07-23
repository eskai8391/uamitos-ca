from typing import Literal, Callable
from presentation.ui.builders.layouts.base_layout_builder import BaseLayoutBuilder
from presentation.ui.builders.layouts.box_layout_builder import BoxLayoutBuilder
from presentation.ui.builders.layouts.form_layout_builder import FormLayoutBuilder
from presentation.ui.builders.layouts.grid_layout_builder import GridLayoutBuilder
from presentation.ui.builders.layouts.stacked_layout_builder import StackedLayoutBuilder

LayoutType = Literal["hbox", "vbox", "form", "grid", "stacked"]

class LayoutFactory:
    def __init__(self):
        self._map: dict[LayoutType, Callable[..., BaseLayoutBuilder]] = {
            "hbox":    lambda **kwargs: BoxLayoutBuilder(**kwargs, orientation = "h"),
            "vbox":    lambda **kwargs: BoxLayoutBuilder(**kwargs, orientation = "v"),
            "form":    lambda **kwargs: FormLayoutBuilder(**kwargs),
            "grid":    lambda **kwargs: GridLayoutBuilder(**kwargs),
            "stacked": lambda **kwargs: StackedLayoutBuilder(**kwargs),
        }

    def get(self, kind: LayoutType, **kwargs) -> BaseLayoutBuilder:
        try:
            factory = self._map[kind]
        except KeyError:
            raise ValueError(f"Layout '{kind}' no soportado")
        return factory(**kwargs)
