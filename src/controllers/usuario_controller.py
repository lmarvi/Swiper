from PySide6.QtWidgets import QDialog, QMessageBox
from src.services.usuario_service import UsuarioService
from src.widgets.dialogo_crear_usuario import UsuarioDialog


class UsuarioController:
    def __init__(self,view):

        self.UsuarioService = UsuarioService(view)
        self.view = view

    def datos_nuevo_usuario(self):
        dialog = UsuarioDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            nuevo_usuario = dialog.get_nuevo_usuario()
            if nuevo_usuario:
                pasar_datos = self.UsuarioService.crear_usuario(nuevo_usuario)
                if pasar_datos:
                    QMessageBox.information(self.view,"Información","Usuario creado con éxito")
                    usuarios = self.UsuarioService.obtener_usarios()
                    self.view.cargar_usuarios(usuarios)

                else:
                    QMessageBox.warning(self.view,"Error","No se pudo crear el usuario")
