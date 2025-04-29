import sys
from PySide6.QtWidgets import QApplication

from src.controllers.login_controller import LoginController
from src.views.main_window import MainWindow
from src.views.login_window import LoginWindow

esAdmin = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window2 = MainWindow()
    login_controller = LoginController(window)
    window.show()
    sys.exit(app.exec())
