import copy
from abc import ABC, abstractmethod
from typing import Self, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy


class BaseWidgetBuilder(ABC):
    """
    Defines the base methods of a widget builder
    """

    # --- Base Functionality of a Builder ---
    def __init__(self):
        """
        Instantiates the base attributes for widgets configurations
        """

        # Widget
        self._widget = None

        # Position and size
        self._x: Optional[int] = None
        self._y: Optional[int] = None
        self._height: Optional[int] = None
        self._width: Optional[int] = None

        # Style properties and fonts
        self._style_sheet: Optional[str] = None
        self._obj_name: Optional[str] = None
        self._font_size: Optional[int] = None
        self._font_bold: Optional[bool] = None
        self._font_family: Optional[str] = None
        self._alignment: Optional[Qt.AlignmentFlag] = None
        self._fixed_width: Optional[int] = None
        self._fixed_height: Optional[int] = None
        self._size_policy_horizontal: Optional[QSizePolicy.Policy] = None
        self._size_policy_vertical: Optional[QSizePolicy.Policy] = None

    def create(self)  -> Self:
        """
        Creates a new instance of the widget builder
        """
        return type(self)()

    def build(self) -> QWidget:
        """
        Builds the widget
        :return: The built widget
        """
        self.__apply_common_properties(self._widget)
        return self._widget

    def clone(self) -> Self:
        """
        Clones the widget
        :return: The cloned widget
        """
        return copy.deepcopy(self)


    # --- Geometry related methods ---
    def set_geometry(self, x: int, y: int, width: int, height: int) -> Self:
        """
        Establishes the positions and size of the widget

        :arg x: The x position of the widget
        :arg y: The y position of the widget
        :arg width: The width of the widget
        :arg height: The height of the widget
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        return self

    def set_fixed_size(self, width: int, height: int) -> Self:
        """
        Establishes a fixed size of the widget

        :arg width: The width of the widget
        :arg height: The height of the widget
        """
        self._fixed_width = width
        self._fixed_height = height
        return self

    def set_size_policy(self, horizontal: QSizePolicy.Policy, vertical: QSizePolicy.Policy) -> Self:
        """
        Establishes a size policy of the widget

        :arg horizontal: The horizontal size of the widget
        :arg vertical: The vertical size of the widget
        """
        self._size_policy_horizontal = horizontal
        self._size_policy_vertical = vertical
        return self


    # --- Styling related methods ---
    def set_style_sheet(self, css: str) -> Self:
        """
        Applies a style sheet to the widget

        :arg css: The style sheet of the widget
        """
        self._style_sheet = css
        return self

    def set_object_name(self, name: str) -> Self:
        self._obj_name = name
        return self

    # --- Font configuration ---
    def set_font_size(self, size: int) -> Self:
        """
        Sets the font size of the widget
        :arg size: The font size of the widget`
        """
        self._font_size = size
        return self

    def set_font_bold(self, bold: bool) -> Self:
        """
        Sets the font bold of the widget
        :arg bold: True if the widgets text should be bold
        """
        self._font_bold = bold
        return self

    def set_font_family(self, family: str) -> Self:
        """
        Sets the font family of the widget
        :arg family: The font family of the widget
        """
        self._font_family = family
        return self


    # --- Alignment configurations ---
    def set_alignment(self, alignment: Qt.AlignmentFlag) -> Self:
        """
        Sets the alignment of the widget
        :arg alignment: The alignment of the widget
        """
        self._alignment = alignment
        return self

    def __apply_common_properties(self, widget: QWidget):
        """
        Auxiliar method to apply common properties
        """
        if self._x is not None and self._y is not None and \
           self._width is not None and self._height is not None:
            widget.setGeometry(self._x, self._y, self._width, self._height)

        if self._fixed_width is not None and self._fixed_height is not None:
            widget.setFixedSize(self._fixed_width, self._fixed_height)

        if self._size_policy_horizontal is not None and self._size_policy_vertical is not None:
            size_policy = QSizePolicy(self._size_policy_horizontal, self._size_policy_vertical)
            widget.setSizePolicy(size_policy)

        if self._obj_name is not None:
            widget.setObjectName(self._obj_name)

        if self._style_sheet is not None:
            widget.setStyleSheet(self._style_sheet)

        # Font configuration
        current_font = widget.font()
        if self._font_size is not None:
            current_font.setPointSize(self._font_size)
        if self._font_bold is not None:
            current_font.setBold(self._font_bold)
        if self._font_family is not None:
            current_font.setFamily(self._font_family)
        widget.setFont(current_font)

        # Alignment configuration
        if self._alignment is not None and hasattr(widget, 'setAlignment'):
            widget.setAlignment(self._alignment)