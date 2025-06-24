import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from Application.UseCases.StudentUseCases import StudentUseCases

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Estudiantes")
        self.setGeometry(100, 100, 400, 500)

        self.use_cases = StudentUseCases()

        self.layout = QVBoxLayout()

        self.fields = {
            "Nombre": QLineEdit(),
            "Apellido": QLineEdit(),
            "Edad": QLineEdit(),
            "Email": QLineEdit(),
            "Tel\u00e9fono": QLineEdit(),
            "Direcci\u00f3n": QLineEdit(),
            "Ciudad": QLineEdit(),
            "Estado": QLineEdit(),
            "C\u00f3digo Postal": QLineEdit(),
            "Contrase\u00f1a": QLineEdit()
        }

        self.fields["Contrase\u00f1a"].setEchoMode(QLineEdit.Password)

        for label, widget in self.fields.items():
            self.layout.addWidget(QLabel(label))
            self.layout.addWidget(widget)

        self.button = QPushButton("Registrar")
        self.button.clicked.connect(self.register_student)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def register_student(self):
        data = {label: widget.text().strip() for label, widget in self.fields.items()}

        if any(v == "" for v in data.values()):
            QMessageBox.warning(self, "Error", "Todos los campos deben estar completos.")
            return

        try:
            student = self.use_cases.register_student(
                name=data["Nombre"],
                last_name=data["Apellido"],
                age=data["Edad"],
                email=data["Email"],
                phone=data["Tel\u00e9fono"],
                address=data["Direcci\u00f3n"],
                city=data["Ciudad"],
                state=data["Estado"],
                zip_code=data["C\u00f3digo Postal"],
                password=data["Contrase\u00f1a"]
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error de validaci\u00f3n", str(e))
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurri\u00f3 un error inesperado: {e}")
            return

        QMessageBox.information(self, "\u00c9xito", f"Estudiante registrado:\n{student}")
        for widget in self.fields.values():
            widget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
