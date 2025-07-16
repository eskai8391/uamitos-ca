from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QSize

class WindowBuilder:
    def __init__(self):
        self.window = QMainWindow()
        self.central_widget = QWidget()
        self.layout = None

    def set_title(self, title):
        self.window.setWindowTitle(title)
        return self

    def set_size(self, w, h):
        self.window.setFixedSize(QSize(w, h))
        return self

    def set_minimum_size(self, w, h):
        self.window.setMinimumSize(QSize(w, h))
        return self

    def set_maximum_size(self, w, h):
        self.window.setMaximumSize(QSize(w, h))
        return self

    def set_layout(self, layout):
        self.layout = layout
        return self

    def build(self):
        self.central_widget.setLayout(self.layout)
        self.window.setCentralWidget(self.central_widget)
        return self.window
