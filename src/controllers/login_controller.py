from PySide6.QtWidgets import QMessageBox
from ..db.conexion_db import ConexionDB
from ..views.main_window import MainWindow


class LoginController:

    def __init__(self,view):

        self.view = view
        self.view.boton_login.clicked.connect(self.login)

    def login(self):

        print("logueando")

        usuario = self.view.usuario_edit.text()
        contrasena = self.view.contrasena_edit.text()

        if not usuario or not contrasena:
            QMessageBox.warning(self.view,
                                "Error",
                                "Introduce usuario y contraseña",
                                QMessageBox.Ok)
            return

        conn = ConexionDB()
        conn.conectar()

        if conn.consulta_login(usuario, contrasena):
            self.view.close()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.warning(self.view, "Error", "Usuario o contraseña incorrectos", QMessageBox.Ok)


