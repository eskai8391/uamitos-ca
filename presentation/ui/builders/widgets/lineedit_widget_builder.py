from PySide6.QtWidgets import QLineEdit
from typing import Self, Literal
from .base_widget_builder import BaseWidgetBuilder

class LineEditWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QLineEdit()

    def set_placeholder(self, text: str) -> Self:
        self._widget.setPlaceholderText(text)
        return self

    def set_echo_mode(self, mode: Literal["Normal", "NoEcho", "Password", "PasswordEchoOnEdit"]) -> Self:
        match mode:
            case "Normal":
                self._widget.setEchoMode(QLineEdit.EchoMode.Normal)

            case "NoEcho":
                self._widget.setEchoMode(QLineEdit.EchoMode.NoEcho)

            case "Password":
                self._widget.setEchoMode(QLineEdit.EchoMode.Password)

            case "PasswordEchoOmEdit":
                self._widget.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        return self