from src.models.esquema import Esquema
from src.services.esquema_service import EsquemaService


class EsquemaController:
    def __init__(self,view):

        self.esquema_service = EsquemaService(view)
        self.view = view

    def get_nuevo_esquema(self,main_window_controller):
        if not main_window_controller:
            return None

        nombre_esquema = self.view.grupo_canales.checkedButton().text()
        colores_entrada = main_window_controller.obtener_nombre_orden_botones_entrada()
        print("Los colores de entrada son: ", colores_entrada)
        colores_salida = main_window_controller.obtener_nombre_orden_botones_salida()
        print("Los colores de salida son: ", colores_salida)

        nuevo_esquema = Esquema(
            esquema_id=None,
            nombre_esquema=nombre_esquema,
            fecha_creacion=None,
            canales_entrada=colores_entrada,
            canales_salida=colores_salida
        )
        return nuevo_esquema
