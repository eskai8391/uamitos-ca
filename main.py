from PySide6.QtWidgets import QApplication
from application.container import AppContainer

def main():
    # Initialize
    app = QApplication([])
    container = AppContainer()

    # Build main window with login page
    window = container.main_window_builder().build()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
