from PySide6.QtWidgets import QDialog, QMessageBox

from src.widgets.dialogo_crear_acceso import NuevoAccesoDialog
from src.services.acceso_service import AccesoService
from src.widgets.dialogo_editar_acceso import EditAccesoDialog


class AccesoController:
    def __init__(self,view):
        self.AccesoService = AccesoService(view)
        self.view = view


    def datos_nuevo_acceso(self):
        dialog = NuevoAccesoDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            nuevo_acceso = dialog.get_nuevo_acceso()
            if nuevo_acceso:
                pasar_datos_acceso = self.AccesoService.crear_acceso(nuevo_acceso)
                if pasar_datos_acceso:
                    QMessageBox.information(self.view, "Información", "Acceso al centro productivo creado con éxito")
                    accesos = self.AccesoService.obtener_accesos()
                    self.view.cargar_accesos(accesos)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido crear el acceso al centro productivo")


    def datos_acceso_editado(self):
        selected_row = self.view.tabla_accesos.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.view, "Error", "Selecciona un acceso para editar")
            return

        # Datos del acceso seleccionado
        acceso_id = int(self.view.tabla_accesos.item(selected_row, 0).text())
        usuario = self.view.tabla_accesos.item(selected_row, 1).text()
        centro = self.view.tabla_accesos.item(selected_row, 2).text()

        # Mostrar el diálogo con los datos actuales
        dialog = EditAccesoDialog(self.view, acceso_id, usuario, centro)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            acceso_editado = dialog.get_acceso_editado()
            if acceso_editado:
                actualizar_acceso = self.AccesoService.editar_acceso(acceso_editado)
                if actualizar_acceso:
                    QMessageBox.information(self.view, "Información", "Acceso editado con éxito")
                    accesos = self.AccesoService.obtener_accesos()
                    self.view.cargar_accesos(accesos)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido editar el acceso")


    def id_acceso(self):
        fila_seleccionada = self.view.tabla_accesos.currentRow()
        id = self.view.tabla_accesos.item(fila_seleccionada, 0).text()
        if fila_seleccionada > 0:
            respuesta = QMessageBox.question(
                self.view,
                "Confirmar acción",
                f"¿Estás seguro que deseas eliminar el acceso?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if respuesta == QMessageBox.Yes:
                acceso_eliminado = self.AccesoService.eliminar_acceso(id)
                if acceso_eliminado:
                    QMessageBox.information(self.view, "Información", f"Acceso eliminado con éxito")
                    accesos = self.AccesoService.obtener_accesos()
                    self.view.cargar_accesos(accesos)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido eliminar el acceso")

        else:
            QMessageBox.warning(self.view,"Error","Selecciona un acceso para eliminar")

