from PySide6.QtWidgets import (
    QLabel, QPushButton, QLineEdit, QRadioButton,
    QGroupBox, QSizePolicy, QVBoxLayout, QTextEdit
)

class WidgetBuilder:
    def __init__(self, widget_type):
        self.widget_type = widget_type
        self.widget = self._create_widget()

    def _create_widget(self):
        if self.widget_type == "label":
            return QLabel()
        elif self.widget_type == "button":
            return QPushButton()
        elif self.widget_type == "lineedit":
            return QLineEdit()
        elif self.widget_type == "textedit":
            return QTextEdit()
        elif self.widget_type == "radiobutton":
            return QRadioButton()
        elif self.widget_type == "groupbox":
            groupbox = QGroupBox()
            groupbox.setLayout(QVBoxLayout())
            return groupbox
        else:
            raise ValueError(f"Unsupported widget_type: {self.widget_type}")

    def set_text(self, text):
        if hasattr(self.widget, "setTitle") and self.widget_type == "groupbox":
            self.widget.setTitle(text)
        elif hasattr(self.widget, "setText"):
            self.widget.setText(text)
        return self

    def add_widget_to_groupbox(self, widget):
        if self.widget_type == "groupbox":
            self.widget.layout().addWidget(widget)
        else:
            raise ValueError("add_widget_to_groupbox can only be used with groupbox")
        return self

    def set_size(self, w, h):
        self.widget.setFixedSize(w, h)
        return self

    def set_style(self, style):
        self.widget.setStyleSheet(style)
        return self

    def set_onclick(self, func):
        if isinstance(self.widget, (QPushButton, QRadioButton)):
            self.widget.clicked.connect(func)
        return self

    def set_size_policy(self, horizontal="preferred", vertical="preferred"):
        policy_map = {
            "fixed": QSizePolicy.Fixed,
            "minimum": QSizePolicy.Minimum,
            "maximum": QSizePolicy.Maximum,
            "preferred": QSizePolicy.Preferred,
            "expanding": QSizePolicy.Expanding,
            "minimumexpanding": QSizePolicy.MinimumExpanding,
            "ignored": QSizePolicy.Ignored
        }

        h_policy = policy_map.get(horizontal.lower(), QSizePolicy.Preferred)
        v_policy = policy_map.get(vertical.lower(), QSizePolicy.Preferred)

        self.widget.setSizePolicy(h_policy, v_policy)
        return self

    def set_word_wrap(self, wrap=True):
        self.widget.setWordWrap(wrap)
        return self

    def to_plain_text(self):
        if isinstance(self.widget, QTextEdit):
            self.widget.toPlainText()
        return self

    def build(self):
        return self.widget
