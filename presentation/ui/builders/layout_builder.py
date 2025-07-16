from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QStackedLayout
)
class LayoutBuilder:
    def __init__(self, layout_type="vbox"):
        if layout_type == "vbox":
            self.layout = QVBoxLayout()
        elif layout_type == "hbox":
            self.layout = QHBoxLayout()
        elif layout_type == "grid":
            self.layout = QGridLayout()
        elif layout_type == "form":
            self.layout = QFormLayout()
        elif layout_type == "stacked":
            self.layout = QStackedLayout()
        else:
            raise ValueError(f"Unsupported layout_type: {layout_type}")

    def add_widget(self, widget, row=None, col=None, rowspan=1, colspan=1, label=None):
        if isinstance(self.layout, QGridLayout):
            if row is None or col is None:
                raise ValueError("GridLayout requires row and col")
            self.layout.addWidget(widget, row, col, rowspan, colspan)
        elif isinstance(self.layout, QFormLayout):
            if label is None:
                raise ValueError("FormLayout requires a label")
            self.layout.addRow(label, widget)
        else:
            self.layout.addWidget(widget)
        return self

    def add_layout(self, layout, row=None, col=None, rowspan=1, colspan=1, stretch=0):
        if isinstance(self.layout, QGridLayout):
            if row is None or col is None:
                raise ValueError("GridLayout requires row and col for adding layout")
            self.layout.addLayout(layout, row, col, rowspan, colspan)
        else:
            self.layout.addLayout(layout, stretch)
        return self

    def set_spacing(self, spacing):
        self.layout.setSpacing(spacing)
        return self

    def set_horizontal_spacing(self, spacing):
        if hasattr(self.layout, 'setHorizontalSpacing'):
            self.layout.setHorizontalSpacing(spacing)
        return self

    def set_vertical_spacing(self, spacing):
        if hasattr(self.layout, 'setVerticalSpacing'):
            self.layout.setVerticalSpacing(spacing)
        return self

    def set_contents_margins(self, left, top, right, bottom):
        self.layout.setContentsMargins(left, top, right, bottom)
        return self

    def build(self):
        return self.layout
