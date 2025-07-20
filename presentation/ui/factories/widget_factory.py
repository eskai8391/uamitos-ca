from typing import Literal, Type

from ..builders.widgets import (ButtonWidgetBuilder, LabelWidgetBuilder, BaseWidgetBuilder,
                                CheckBoxWidgetBuilder, ComboBoxWidgetBuilder, LineEditWidgetBuilder,
                                StackedWidgetBuilder)

WidgetType = Literal["button", "label", "lineedit", "checkbox", "combobox", "stacked"]

class WidgetFactory:
    def __init__(self):
        self.__builders_map: dict[WidgetType, Type[BaseWidgetBuilder]] = {
            "button": ButtonWidgetBuilder,
            "label": LabelWidgetBuilder,
            "lineedit": LineEditWidgetBuilder,
            "checkbox": CheckBoxWidgetBuilder,
            "combobox": ComboBoxWidgetBuilder,
            "stacked": StackedWidgetBuilder
        }

    def get(self, kind:WidgetType) -> BaseWidgetBuilder:
        try:
            builder_cls = self.__builders_map[kind]
        except KeyError:
            raise KeyError(f"Unknown widget type: {kind}")
        return builder_cls().create()