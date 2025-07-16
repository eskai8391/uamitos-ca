from abc import ABC, abstractmethod
from typing import Self, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy


class BaseWidgetBuilder(ABC):
    # --- Base Functionality of a Builder ---
    """
    Defines the base methods of a widget builder
    """
    def __init__(self):
        """
        Instantiates the base attributes for widgets configurations
        """

        # Position and size
        self.__x: Optional[int] = None
        self.__y: Optional[int] = None
        self.__height: Optional[int] = None
        self.__width: Optional[int] = None

        # Style properties and fonts
        self.__style_sheet: Optional[str] = None
        self.__font_size: Optional[int] = None
        self.__font_bold: Optional[bool] = None
        self.__font_family: Optional[str] = None
        self.__alignment: Optional[Qt.AlignmentFlag] = None
        self.__fixed_width: Optional[int] = None
        self.__fixed_height: Optional[int] = None
        self.__size_policy_horizontal: Optional[QSizePolicy.Policy] = None
        self.__size_policy_vertical: Optional[QSizePolicy.Policy] = None


    def create(self)  -> Self:
        """
        Creates a new instance of the widget builder
        """
        return type(self)()

    @abstractmethod
    def build(self) -> QWidget:
        """
        Builds the widget
        :return:
        """
        pass

    # --- Geometry related methods ---
    def set_geometry(self, x: int, y: int, width: int, height: int) -> Self:
        """
        Establishes the positions and size of the widget

        :arg x: The x position of the widget
        :arg y: The y position of the widget
        :arg width: The width of the widget
        :arg height: The height of the widget
        """
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        return self

    def set_fixed_size(self, width: int, height: int) -> Self:
        """
        Establishes a fixed size of the widget

        :arg width: The width of the widget
        :arg height: The height of the widget
        """
        self.__fixed_width = width
        self.__fixed_height = height
        return self

    def set_size_policy(self, horizontal: QSizePolicy.Policy, vertical: QSizePolicy.Policy) -> Self:
        """
        Establishes a size policy of the widget

        :arg horizontal: The horizontal size of the widget
        :arg vertical: The vertical size of the widget
        """
        self.__size_policy_horizontal = horizontal
        self.__size_policy_vertical = vertical
        return self

    # --- Styling related methods ---
    def set_style_sheet(self, css: str) -> Self:
        """
        Applies a style sheet to the widget

        :arg css: The style sheet of the widget
        """
        self.__style_sheet = css
        return self

    # --- Font configuration ---
    def set_font_size(self, size: int) -> Self:
        """
        Sets the font size of the widget
        :arg size: The font size of the widget`
        """
        self.__font_size = size
        return self

    def set_font_bold(self, bold: bool) -> Self:
        """
        Sets the font bold of the widget
        :arg bold: True if the widgets text should be bold
        """
        self.__font_bold = bold
        return self

    def set_font_family(self, family: str) -> Self:
        """
        Sets the font family of the widget
        :arg family: The font family of the widget
        """
        self.__font_family = family
        return self

    # --- Alignment configurations ---
    def set_alignment(self, alignment: Qt.AlignmentFlag) -> Self:
        """
        Sets the alignment of the widget
        :arg alignment: The alignment of the widget
        """
        self.__alignment = alignment
        return self

    def __apply_common_properties(self, widget: QWidget):
        """
        Auxiliar method to apply common properties
        """
        if self.__x is not None and self.__y is not None and \
           self.__width is not None and self.__height is not None:
            widget.setGeometry(self.__x, self.__y, self.__width, self.__height)

        if self.__fixed_width is not None and self.__fixed_height is not None:
            widget.setFixedSize(self.__fixed_width, self.__fixed_height)

        if self.__size_policy_horizontal is not None and self.__size_policy_vertical is not None:
            size_policy = QSizePolicy(self.__size_policy_horizontal, self.__size_policy_vertical)
            widget.setSizePolicy(size_policy)

        if self.__style_sheet is not None:
            widget.setStyleSheet(self.__style_sheet)

        # Font configuration
        current_font = widget.font()
        if self.__font_size is not None:
            current_font.setPointSize(self.__font_size)
        if self.__font_bold is not None:
            current_font.setBold(self.__font_bold)
        if self.__font_family is not None:
            current_font.setFamily(self.__font_family)
        widget.setFont(current_font)

        # Alignment configuration
        if self.__alignment is not None and hasattr(widget, 'setAlignment'):
            widget.setAlignment(self.__alignment)