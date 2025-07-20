from PySide6.QtWidgets import (
    QWidget, QLineEdit, QMessageBox
)
from typing import Callable

from presentation.ui.builders.views.components.phantom_button import PhantomButton
from presentation.ui.factories import WidgetFactory, LayoutFactory


class LoginWidgetBuilder:
    def __init__(
        self,
        widget_factory: WidgetFactory,
        layout_factory : LayoutFactory,
        on_login: Callable[[str, str], None] = lambda u, p: None
    ):
        self.__main_layout = layout_factory.get("vbox")\
            .create()

        self.__form_layout = layout_factory.get("form")\
            .create()

        self.__form_email_input = widget_factory.get("lineedit")\
            .create()\
            .set_placeholder("Correo electrónico")\
            .build()

        self.__form_password_input = widget_factory.get("lineedit")\
            .create()\
            .set_placeholder("Contraseña")\
            .set_echo_mode(QLineEdit.Password)\
            .build()

        self.__form_btn = widget_factory.get("button")\
            .create()\
            .set_text("Iniciar sesión")\
            .build()

        self.__form_layout.add_row("Usuario:", self.__form_email_input)
        self.__form_layout.add_row("Contraseña:", self.__form_password_input)

        self.__main_layout.add_layout(self.__form_layout.build(), 1)
        self.__main_layout.add_widget(self.__form_btn)

        self.__main_widget = QWidget()
        self.__main_widget.setLayout(self.__main_layout.build())

    def build(self) -> QWidget:
        return self.__main_widget