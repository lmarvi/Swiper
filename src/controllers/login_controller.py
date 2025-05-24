from PySide6.QtWidgets import QMessageBox
from ..db.conexion_db import ConexionDB
from ..services.login_service import LoginService
from ..views.main_window import MainWindow


class LoginController:

    def __init__(self,view):

        self.main_window = None
        self.view = view
        self.login_service = LoginService(self.view)
        self.usuario = None

    def login(self):
        self.usuario = self.view.usuario_edit.text()
        contrasena = self.view.contrasena_edit.text()

        if not self.usuario or not contrasena:
            QMessageBox.warning(self.view.parentWidget(),
                                "Error",
                                "Introduce usuario y contraseña",
                                QMessageBox.Ok)
            return


        if self.login_service.consulta_login(self.usuario,contrasena):
            es_admin = self.es_admin()
            print(f"Usuario {self.usuario} es admin: {es_admin}")
            nombre_centro = self.view.accesos_combobox.currentText()
            nombre_usuario = self.view.usuario_edit.text()
            self.main_window = MainWindow()
            self.main_window.configurar_interfaz(es_admin,nombre_usuario,nombre_centro)
            self.view.parentWidget().close()
            self.main_window.show()
        else:
            QMessageBox.warning(self.view.parentWidget(), "Error", "Usuario o contraseña incorrectos", QMessageBox.Ok)

    def usuario_accesos(self):
        usuario = self.view.usuario_edit.text()

        if usuario:
            lista_accesos = self.login_service.consulta_usuario_accesos(usuario)
            self.view.accesos_combobox.addItems(lista_accesos)

    def es_admin(self):
        usuario = self.usuario
        admin = "admin"
        es_admin = True
        rol = self.login_service.consulta_rol(usuario)
        rol_limpio = rol.strip().lower()
        print("Rol obtenido:", rol_limpio)
        if rol_limpio == admin:
            return es_admin
        else:
            es_admin = False
            return  es_admin


