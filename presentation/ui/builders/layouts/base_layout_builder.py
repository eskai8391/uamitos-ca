# presentation/ui/builders/base_layout_builder.py
import copy
from abc import ABC, abstractmethod
from typing import Self, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLayout, QWidget, QSizePolicy
)

class BaseLayoutBuilder(ABC):
    """
    Defines the base methods of a layout builder
    """

    def __init__(self):
        """
        Instantiates the base attributes for layouts configurations
        """

        self._margin: Optional[int] = None
        self._spacing: Optional[int] = None
        self._alignment: Optional[Qt.AlignmentFlag] = None
        self._stretch_factors: list[int] = []
        self._fixed_width: Optional[int] = None
        self._fixed_height: Optional[int] = None
        self._layout: Optional[QLayout] = None

    def create(self) -> Self:
        """
        Creates a new instance of the layout builder
        """
        return type(self)()

    @abstractmethod
    def build(self) -> QLayout:
        """
        Builds the layout
        :return: The built layout
        """
        pass

    def clone(self) -> Self:
        """
        Clones the layout
        :return: The cloned layout
        """
        return copy.deepcopy(self)

    @property
    def margin(self) -> int:
        return self._margin

    @property
    def spacing(self) -> int:
        return self._spacing

    @property
    def alignment(self) -> Qt.AlignmentFlag:
        return self._alignment

    @property
    def stretch_factors(self) -> list[int]:
        return self._stretch_factors

    @property
    def fixed_width(self) -> int:
        return self._fixed_width

    @property
    def fixed_height(self) -> int:
        return self._fixed_height

    @property
    def layout(self) -> QLayout:
        return self._layout

    @abstractmethod
    def add_widget(self, widget: QWidget) -> Self:
        pass

    def set_margin(self, margin: int) -> Self:
        """
        Sets the margin
        :param margin: The margin to set
        """
        self._margin = margin
        return self

    def set_spacing(self, spacing: int) -> Self:
        """
        Sets the spacing
        :param spacing: The spacing to set
        """
        self._spacing = spacing
        return self

    def set_alignment(self, alignment: Qt.AlignmentFlag) -> Self:
        """
        Sets the alignment
        :param alignment: The alignment to set
        """
        self._alignment = alignment
        return self

    def set_fixed_size(self, width: int, height: int) -> Self:
        """
        Sets the fixed size
        :param width: The width to set
        :param height: The height to set
        """
        self._fixed_width = width
        self._fixed_height = height
        return self

    def _apply_common(self, layout: QLayout, container: QWidget):
        """
        Applies the common layout
        :param layout: The layout to apply
        :param container: The container to apply the layout
        """
        if self._margin is not None:
            layout.setContentsMargins(*([self._margin] * 4))
        if self._spacing is not None:
            layout.setSpacing(self._spacing)
        if self._alignment is not None and hasattr(container, "setAlignment"):
            container.setAlignment(self._alignment)
        if self._fixed_width and self._fixed_height:
            container.setFixedSize(self._fixed_width, self._fixed_height)
