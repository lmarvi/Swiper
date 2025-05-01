from PySide6.QtWidgets import QMessageBox
from ..db.conexion_db import ConexionDB
from ..views.main_window import MainWindow


class LoginController:

    def __init__(self,view):

        self.view = view
        self.view.boton_login.clicked.connect(self.login)



    ## def accesos(self):


    def login(self):

        print("logueando")

        self.usuario = self.view.usuario_edit.text()
        self.contrasena = self.view.contrasena_edit.text()

        if not self.usuario or not self.contrasena:
            QMessageBox.warning(self.view,
                                "Error",
                                "Introduce usuario y contraseña",
                                QMessageBox.Ok)
            return

        self.conn = ConexionDB()
        self.conn.conectar()

        if self.conn.consulta_login(self.usuario,self.contrasena):
            esAdmin = self.es_admin()
            print(f"Usuario {self.usuario} es admin: {esAdmin}")
            self.main_window = MainWindow()
            self.main_window.configurar_interfaz(esAdmin)
            self.view.close()
            self.main_window.show()
        else:
            QMessageBox.warning(self.view, "Error", "Usuario o contraseña incorrectos", QMessageBox.Ok)

    def es_admin(self):
        usuario = self.usuario
        admin = "admin"
        esAdmin = True
        rol = self.conn.consulta_rol(usuario)
        rol_limpio = rol.strip().lower()
        print("Rol obtenido:", rol_limpio)
        if rol_limpio == admin:
            return esAdmin
        else:
            esAdmin = False
            return  esAdmin


