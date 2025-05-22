import sys
from PySide6.QtWidgets import QApplication

from src.config.inicializar_config import inicializar_rutas_config
from src.controllers.login_controller import LoginController
from src.views.login_window import LoginWindow
from src.views.main_window import MainWindow

esAdmin = False

if __name__ == "__main__":
    inicializar_rutas_config()
    app = QApplication(sys.argv)
    window = LoginWindow()

    login_controller = LoginController(window)
    window.show()
    sys.exit(app.exec())
