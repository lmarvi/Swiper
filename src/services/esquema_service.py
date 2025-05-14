from PySide6.QtWidgets import QMessageBox
from src.db.conexion_db import ConexionDB


class EsquemaService:
    def __init__(self,view):
        self.view = view
        self._conn = ConexionDB()
        self._conn.conectar()

    def guardar_esquema(self,nuevo_esquema):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO esquemas (nombre,canales_entrada,canales_salida)
                    VALUES (%s,%s,%s) RETURNING esquema_id""",
                    (nuevo_esquema.nombre_esquema,nuevo_esquema.canales_entrada,nuevo_esquema.canales_salida))
                nuevo_id = cursor.fetchone()[0]
                self._conn.commit()
                return nuevo_id
        except Exception as e:
            print(f"Error en la inserción del esquema: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al guardar el esquema: {e}"
            )
            return None