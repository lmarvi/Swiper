import os
from PySide6.QtWidgets import QMessageBox
from src.services.procesado_service import ProcesadoService


class ProcesadoController:
    def __init__(self,main_window_controller):
        self.mwc = main_window_controller
        self.view = main_window_controller.view

    def iniciar_procesado(self):

        lista_disenos = self.mwc.get_lista_disenos()
        print(lista_disenos)

        if not lista_disenos:
            QMessageBox.warning(self.view, "Error", "No hay diseños para procesar")
            return

        ruta_salida = self.mwc.get_ruta_salida()

        procesado_service = ProcesadoService(self.view)

        for diseno in lista_disenos:
            procesado = procesado_service.procesado(diseno, ruta_salida)

            if procesado:
                nombre = os.path.basename(diseno)
                # 1. eliminar del widget
                for row in range(self.view.lista_disenos.count() - 1, -1, -1):
                    item = self.view.lista_disenos.item(row)
                    if item.text() == nombre:
                        self.view.lista_disenos.takeItem(row)
                # 2. eliminar del diccionario
                del self.mwc.disenos_rutas[nombre]
            else:
                QMessageBox.warning(self.view, "Error", "No se han podido procesar los archivos")

        QMessageBox.information(self.view, "Información", "Procesado terminado")

