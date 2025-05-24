from PySide6.QtWidgets import QWidget, QVBoxLayout

from src.controllers.crear_db_controller import CrearDBController
from src.controllers.login_controller import LoginController
from src.ui.login_ui import LoginUI


class LoginWindow(QWidget):
    def __init__(self):
        crear_db = CrearDBController()
        crear_db.inicializar_db()

        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(850, 350, 100, 150)

        main_layout = QVBoxLayout(self)
        self.ui = LoginUI()
        main_layout.addWidget(self.ui)

        self._controller_login = LoginController(self.ui)

        self.ui.boton_login.clicked.connect(self._controller_login.login)
        self.ui.usuario_edit.textChanged.connect(self._controller_login.usuario_accesos)
