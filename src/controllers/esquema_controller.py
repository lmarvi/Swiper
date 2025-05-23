from PySide6.QtWidgets import QMessageBox
from src.models.esquema import Esquema
from src.services.centro_service import CentroService
from src.services.esquema_service import EsquemaService


class EsquemaController:
    def __init__(self,view):

        self.esquema_service = EsquemaService(view)
        self.view = view

    def anadir_esquema(self,nuevo_esquema,nombre_centro):
        esquema_id = self.esquema_service.guardar_esquema(nuevo_esquema)
        if esquema_id:
            self.esquema_service.anadir_esquema_a_centro(esquema_id, nombre_centro)
            QMessageBox.information(
                self.view,
                "Éxito",
                f"Esquema '{nuevo_esquema.nombre_esquema}' guardado correctamente."
            )
            self.view.cargar_datos_centros()
            return True
        else:
            QMessageBox.warning(
                self.view,
                "Error",
                "No se ha podido guardar el esquema."
            )
            return False

    def get_nuevo_esquema(self, main_window_controller):
        if not main_window_controller:
            return None

        btn = self.view.grupo_esquemas.checkedButton()
        if not btn:
            QMessageBox.warning(self.view, "Error", "Selecciona un esquema para guardar")
            return None

        nombre_esquema = btn.text()

        # Obtener el id si ya existe en el diccionario
        esquema_id = None
        if nombre_esquema in main_window_controller.esquemas_ids:
            esquema_id = main_window_controller.esquemas_ids[nombre_esquema]

        colores_entrada = main_window_controller.obtener_nombre_orden_botones_entrada()
        colores_salida = main_window_controller.obtener_nombre_orden_botones_salida()

        nuevo_esquema = Esquema(
            esquema_id=esquema_id,
            nombre_esquema=nombre_esquema,
            fecha_creacion=None,
            canales_entrada=colores_entrada,
            canales_salida=colores_salida
        )
        return nuevo_esquema

    def get_nombre_esquema(self):
        btn = self.view.grupo_esquemas.checkedButton()
        if btn is None:
            QMessageBox.warning(self.view, "Error", "Ningún esquema seleccionado")
            return False

        nombre_esquema_seleccionado = btn.text()
        return nombre_esquema_seleccionado

    def esquema_a_eliminar(self, main_window_controller,nombre_centro):
        """Elimina el esquema seleccionado de la BD y de la interfaz"""
        btn = self.view.grupo_esquemas.checkedButton()
        if btn is None:
            QMessageBox.warning(self.view, "Error", "Ningún esquema seleccionado")
            return False

        nombre_esquema_seleccionado = self.get_nombre_esquema()

        respuesta = QMessageBox.question(
            self.view,
            "Confirmar acción",
            f"¿Estás seguro que deseas eliminar el esquema {nombre_esquema_seleccionado}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if respuesta == QMessageBox.Yes:
            esquema_seleccionado_id = self.esquema_service.get_esquema_id(nombre_esquema_seleccionado)
            if esquema_seleccionado_id:
                # Eliminar esquema de la db
                esquema_eliminado = self.esquema_service.eliminar_esquema(esquema_seleccionado_id,nombre_centro)
                if esquema_eliminado:
                    # Eliminar de la interfaz
                    self.view.grupo_esquemas.removeButton(btn)
                    self.view.layout_esquemas_draganddrop.removeWidget(btn)
                    btn.setParent(None)
                    btn.deleteLater()

                    # Eliminar del diccionario de ids si existe
                    if nombre_esquema_seleccionado in main_window_controller.esquemas_ids:
                        del main_window_controller.esquemas_ids[nombre_esquema_seleccionado]

                    # Limpiar los canales de entrada y salida
                    main_window_controller.limpiar_canales()
                    self.view.cargar_datos_centros()
                    QMessageBox.information(
                        self.view,
                        "Información",
                        f"Esquema {nombre_esquema_seleccionado} eliminado con éxito"
                    )
                    return True
                else:
                    QMessageBox.warning(self.view, "Error", "No se ha podido eliminar el esquema")
            else:
                # Si no tiene ID es porque es un esquema nuevo que no existe en la BD
                # Eliminar solo de la interfaz
                self.view.grupo_esquemas.removeButton(btn)
                self.view.layout_esquemas_draganddrop.removeWidget(btn)
                btn.setParent(None)
                btn.deleteLater()

                # Eliminar del diccionario si existe
                if nombre_esquema_seleccionado in main_window_controller.esquemas_ids:
                    del main_window_controller.esquemas_ids[nombre_esquema_seleccionado]

                # Limpiar los canales
                main_window_controller.limpiar_canales()

                QMessageBox.information(
                    self.view,
                    "Información",
                    f"Esquema {nombre_esquema_seleccionado} eliminado"
                )
                return True

        return False

    def obtener_id_esquema_seleccionado(self):
        """Obtiene el ID del esquema actualmente seleccionado"""
        btn = self.view.grupo_canales.checkedButton()
        if btn is None:
            return None

        nombre_esquema = btn.text()
        # Buscamos el ID en la db
        esquema_id = self.esquema_service.get_esquema_id(nombre_esquema)
        return esquema_id

    def cargar_esquemas(self, main_window_controller, nombre_centro):
        """Carga los esquemas de la base de datos y los muestra en la interfaz"""
        esquemas = self.esquema_service.obtener_todos_esquemas(nombre_centro)
        if esquemas:
            # Limpiar los esquemas actuales antes de cargar los nuevos
            main_window_controller.limpiar_esquemas()

            # Añadir cada esquema a la interfaz
            for esquema in esquemas:
                esquema_id = esquema[0]
                nombre = esquema[1]
                # Añadir a la interfaz
                main_window_controller.anadir_esquema_desde_db(nombre, esquema_id)

            return True
        return False

    def cargar_detalle_esquema(self, main_window_controller, esquema_id):
        """Carga los detalles de un esquema y muestra sus canales"""
        if esquema_id is None:
            return False  # No cargar nada para esquemas nuevos sin ID
        esquema = self.esquema_service.obtener_esquema_completo(esquema_id)
        if esquema:
            # Cargar canales de entrada y salida
            main_window_controller.cargar_canales_entrada(esquema['canales_entrada'])
            main_window_controller.cargar_canales_salida(esquema['canales_salida'])
            return True
        return False