from PySide6.QtWidgets import QDialog, QMessageBox

from src.services.acceso_service import AccesoService
from src.widgets.dialogo_crear_centro import NuevoCentroDialog
from src.services.centro_service import CentroService
from src.widgets.dialogo_editar_centro import EditCentroDialog


class CentroController:
    def __init__(self,view):
        self.centro_service = CentroService(view)
        self.acceso_service = AccesoService(view)
        self.view = view

    def datos_nuevo_centro(self):
        dialog = NuevoCentroDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            nuevo_centro = dialog.get_nuevo_centro()
            if nuevo_centro:
                pasar_datos_centro = self.centro_service.crear_centro(nuevo_centro)
                if pasar_datos_centro:
                    QMessageBox.information(self.view, "Información", "Centro creado con éxito")
                    centros = self.centro_service.obtener_centros()
                    self.view.cargar_centros(centros)
                    accesos = self.acceso_service.obtener_accesos()
                    self.view.cargar_accesos(accesos)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido crear el centro")

    def datos_centro_editado(self):
        selected_row = self.view.tabla_centros.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.view,"Error","Selecciona un centro productivo para editar")
            return

        # Datos del centro seleccionado
        centro_id = int(self.view.tabla_centros.item(selected_row, 0).text())
        nombre = self.view.tabla_centros.item(selected_row, 1).text()

        # Mostrar el diálogo con los datos actuales
        dialog = EditCentroDialog(self.view, centro_id,nombre)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            centro_editado = dialog.get_centro_editado()
            if centro_editado:
                actualizar_centro = self.centro_service.editar_centro(centro_editado)
                if actualizar_centro:
                    QMessageBox.information(self.view, "Información", "Centro productivo editado con éxito")
                    centros = self.centro_service.obtener_centros()
                    self.view.cargar_centros(centros)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido editar el centro")

    def elminar_id_centro(self):
        fila_seleccionada = self.view.tabla_centros.currentRow()
        nombre = self.view.tabla_centros.item(fila_seleccionada, 1).text()
        id = self.view.tabla_centros.item(fila_seleccionada, 0).text()
        if fila_seleccionada > 0:
            respuesta = QMessageBox.question(
                self.view,
                "Confirmar acción",
                f"¿Estás seguro que deseas eliminar a {nombre}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if respuesta == QMessageBox.Yes:
                centro_eliminado = self.centro_service.eliminar_centro(id)
                if centro_eliminado:
                    QMessageBox.information(self.view, "Información", f"Centro productivo {nombre} eliminado con éxito")
                    centros = self.centro_service.obtener_centros()
                    self.view.cargar_centros(centros)
                    accesos = self.acceso_service.obtener_accesos()
                    self.view.cargar_accesos(accesos)
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido eliminar el centro productivo")

        else:
            QMessageBox.warning(self.view,"Error","Selecciona un centro productivo")

