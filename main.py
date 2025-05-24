import sys
from PySide6.QtWidgets import QApplication
from src.controllers.login_controller import LoginController
from src.views.login_window import LoginWindow


esAdmin = False

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = LoginWindow()

    login_controller = LoginController(window)
    window.show()
    sys.exit(app.exec())
