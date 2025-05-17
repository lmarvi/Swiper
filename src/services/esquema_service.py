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
                if nuevo_esquema.esquema_id is None:
                    # Es un nuevo esquema
                    cursor.execute(
                        """INSERT INTO esquemas (nombre, canales_entrada, canales_salida)
                        VALUES (%s, %s, %s) RETURNING esquema_id""",
                        (nuevo_esquema.nombre_esquema, nuevo_esquema.canales_entrada, nuevo_esquema.canales_salida))
                    nuevo_id = cursor.fetchone()[0]
                    self._conn.commit()
                    self.view.boton_editar_esquema.setChecked(False)
                    return nuevo_id
                else:
                    # Es una actualización
                    cursor.execute(
                        """UPDATE esquemas SET nombre = %s, canales_entrada = %s, canales_salida = %s
                        WHERE esquema_id = %s RETURNING esquema_id""",
                        (nuevo_esquema.nombre_esquema, nuevo_esquema.canales_entrada, nuevo_esquema.canales_salida, nuevo_esquema.esquema_id))
                    esquema_id = cursor.fetchone()[0]
                    self._conn.commit()
                    return esquema_id
        except Exception as e:
            print(f"Error en la inserción del esquema: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al guardar el esquema: {e}"
            )
            return None

    def eliminar_esquema(self, esquema_id):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM esquemas WHERE esquema_id = %s RETURNING esquema_id""",
                    (esquema_id,))
                resultado = cursor.fetchone()
                self._conn.commit()
                return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error en la eliminación del esquema: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al eliminar el esquema: {e}"
            )
            return None

    def get_esquema_id(self,esquema):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """SELECT esquema_id FROM esquemas WHERE nombre = %s""",
                    (esquema,))
                esquema_id = cursor.fetchone()[0]
                return esquema_id
        except Exception as e:
            print(f"Error en la consulta del esquema: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al consultar el id del esquema: {e}"
            )
            return None

    def obtener_todos_esquemas(self):
        """Obtiene todos los esquemas de la base de datos"""
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """SELECT esquema_id, nombre, canales_entrada, canales_salida 
                    FROM esquemas ORDER BY nombre"""
                )
                esquemas = cursor.fetchall()
                return esquemas
        except Exception as e:
            print(f"Error al obtener esquemas: {e}")
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al cargar los esquemas: {e}"
            )
            return []

    def obtener_esquema_completo(self, esquema_id):
        """Obtiene detalles completos de un esquema por su ID"""
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """SELECT esquema_id, nombre, canales_entrada, canales_salida 
                    FROM esquemas WHERE esquema_id = %s""",
                    (esquema_id,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    return {
                        'id': resultado[0],
                        'nombre': resultado[1],
                        'canales_entrada': resultado[2],
                        'canales_salida': resultado[3]
                    }
                return None
        except Exception as e:
            print(f"Error al obtener detalles del esquema: {e}")
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al cargar los detalles del esquema: {e}"
            )
            return None