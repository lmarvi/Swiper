from PySide6.QtWidgets import QDialog, QMessageBox
from src.services.usuario_service import UsuarioService
from src.widgets.dialogo_crear_usuario import NuevoUsuarioDialog
from src.widgets.dialogo_editar_usuario import EditUsuarioDialog


class UsuarioController:
    def __init__(self,view):

        self.usuario_service = UsuarioService(view)
        self.view = view

    def datos_nuevo_usuario(self):
        dialog = NuevoUsuarioDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            nuevo_usuario = dialog.get_nuevo_usuario()
            if nuevo_usuario:
                pasar_datos = self.usuario_service.crear_usuario(nuevo_usuario)
                if pasar_datos:
                    QMessageBox.information(self.view,"Información","Usuario creado con éxito")
                    usuarios = self.usuario_service.obtener_usuarios()
                    self.view.cargar_usuarios(usuarios)
                else:
                    QMessageBox.warning(self.view,"Error","No se ha podido crear el usuario")

    def datos_usuario_editado(self):
        selected_row = self.view.tabla_usuarios.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.view,"Error","Selecciona un usuario para editar")
            return

        # Datos del usuario seleccionado
        usuario_id = int(self.view.tabla_usuarios.item(selected_row, 0).text())
        nombre = self.view.tabla_usuarios.item(selected_row, 1).text()
        contrasena = self.view.tabla_usuarios.item(selected_row, 2).text()
        rol = self.view.tabla_usuarios.item(selected_row, 3).text()

        # Mostrar el diálogo con los datos actuales
        dialog = EditUsuarioDialog(self.view, usuario_id, nombre, contrasena, rol)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            usuario_editado = dialog.get_usuario_editado()
            if usuario_editado:
                actualizar_usuario = self.usuario_service.editar_usuario(usuario_editado)
                if actualizar_usuario:
                    QMessageBox.information(self.view, "Información", "Usuario editado con éxito")
                    usuarios = self.usuario_service.obtener_usuarios()
                    self.view.cargar_usuarios(usuarios)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido editar el usuario")

    def eliminar_id_usuario(self):
        fila_seleccionada = self.view.tabla_usuarios.currentRow()
        nombre = self.view.tabla_usuarios.item(fila_seleccionada, 1).text()
        id = self.view.tabla_usuarios.item(fila_seleccionada, 0).text()
        if fila_seleccionada > 0:
            respuesta = QMessageBox.question(
                self.view,
                "Confirmar acción",
                f"¿Estás seguro que deseas eliminar a {nombre}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if respuesta == QMessageBox.Yes:
                usuario_eliminado = self.usuario_service.eliminar_usuario(id)
                if usuario_eliminado:
                    QMessageBox.information(self.view, "Información", f"Usuario {nombre} eliminado con éxito")
                    usuarios = self.usuario_service.obtener_usuarios()
                    self.view.cargar_usuarios(usuarios)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido eliminar el usuario")

        else:
            QMessageBox.warning(self.view,"Error","Selecciona un usuario")