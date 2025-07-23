from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QMessageBox
)
import os
from typing import Callable

from presentation.ui.builders.views.components.phantom_button import PhantomButton
from presentation.ui.factories import WidgetFactory, LayoutFactory


class LoginWidgetBuilder:
    def __init__(
        self,
        wf: WidgetFactory,
        lf : LayoutFactory,
        on_login: Callable[[str, str], None] = lambda u, p: None
    ):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        style_path = os.path.join(current_dir, "login_styles.qss")

        self.__main_layout = (
            lf.get("vbox", is_container = True)
            .set_style_sheet(route = style_path)
            .set_alignment(Qt.AlignmentFlag.AlignCenter)
            .set_class("container")
        )

        self.__welcome_layout = (
            lf.get("vbox")
            .add_widget((
                wf.get("label")
                .set_text("Bienvenido!")
                .set_font_size(16)
                .set_font_bold(True)
                .build()
            ))
            #.add_widget((
            #    wf.get("label")
            #    .set_text("Inicia sesión para continuar")
            #    .set_font_size(12)
            #    .build()
            #))
        )

        self.__form_layout = lf.get("form")
        self.__form_input_email = (
            wf.get("lineedit")
            .set_placeholder("Correo Electrónico")
            .build()
        )
        self.__form_input_password = (
            wf.get("lineedit")
            .set_placeholder("Contraseña")
            .set_echo_mode("Password")
            .build()
        )
        self.__form_button = (
            wf.get("button")
            .set_text("Iniciar sesión")
            .build()
        )

        (self.__form_layout
         .add_row("", self.__form_input_email)
         .add_row("", self.__form_input_password)
         .add_row("", self.__form_button)
         )

        self.__main_layout.add_layout(self.__welcome_layout.build(), 1)
        self.__main_layout.add_layout(self.__form_layout.build(), 1)

    def build(self) -> QWidget:
        return self.__main_layout.build()