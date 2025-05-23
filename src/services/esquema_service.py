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
                    self._conn._conn.commit()
                    self.view.boton_editar_esquema.setChecked(False)
                    print(f"Esquema guardado con ID: {nuevo_id}")
                    return nuevo_id
                else:
                    # Es una actualización
                    cursor.execute(
                        """UPDATE esquemas SET nombre = %s, canales_entrada = %s, canales_salida = %s
                        WHERE esquema_id = %s RETURNING esquema_id""",
                        (nuevo_esquema.nombre_esquema, nuevo_esquema.canales_entrada, nuevo_esquema.canales_salida, nuevo_esquema.esquema_id))
                    esquema_id = cursor.fetchone()[0]
                    self._conn._conn.commit()
                    print(f"Esquema actualizado con ID: {esquema_id}")
                    return esquema_id
        except Exception as e:
            print(f"Error en la inserción del esquema: {e}")
            self._conn._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al guardar el esquema: {e}"
            )
            return None

    def anadir_esquema_a_centro(self, esquema_id, nombre_centro):
        try:
            with self._conn.cursor() as cursor:
                # Primero obtenemos los esquemas_ids actuales del centro
                cursor.execute(
                    """SELECT esquemas_ids FROM centros_productivos WHERE nombre = %s""",
                    (nombre_centro,)
                )
                esquemas_actuales_resultado = cursor.fetchone()

                if esquemas_actuales_resultado and esquemas_actuales_resultado[0]:
                    # Si ya tiene esquemas, añadimos el nuevo
                    esquemas_actuales = esquemas_actuales_resultado[0]
                    if esquema_id not in esquemas_actuales:
                        esquemas_actuales.append(esquema_id)
                    esquemas_ids = esquemas_actuales
                else:
                    # Si no tiene esquemas, creamos un array con solo el nuevo
                    esquemas_ids = [esquema_id]

                # Actualizar el centro con el nuevo array de esquemas
                cursor.execute(
                    """UPDATE centros_productivos SET esquemas_ids = %s
                    WHERE nombre = %s RETURNING centro_id""",
                    (esquemas_ids, nombre_centro))
                centro_id = cursor.fetchone()[0]
                self._conn.commit()
                return centro_id
        except Exception as e:
            print(f"Error en la inserción del centro: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al guardar el esquema en el centro productivo: {e}"
            )
            return None

    def eliminar_esquema(self, esquema_id, nombre_centro):
        try:
            with self._conn.cursor() as cursor:
                # Obtenemos los esquemas_ids actuales del centro
                cursor.execute(
                    """SELECT esquemas_ids FROM centros_productivos WHERE nombre = %s""",
                    (nombre_centro,)
                )
                resultado = cursor.fetchone()
                if not resultado:
                    QMessageBox.warning(
                        None,  # Asegúrate de reemplazar esto con tu ventana principal
                        "Error",
                        f"No se encontró el centro productivo '{nombre_centro}'."
                    )
                    return None
                # El resultado es una tupla, y el primer elemento es el array
                lista_esquemas_ids = resultado[0]

                # Verificar si el esquema está en la lista
                if esquema_id not in lista_esquemas_ids:
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        f"El esquema con ID {esquema_id} no está asignado a este centro."
                    )
                    return None

                # Creamos una nueva lista sin el esquema a eliminar
                lista_esquemas_ids_nueva = [i for i in lista_esquemas_ids if i != esquema_id]

                # Actualizar el centro con el nuevo array de esquemas
                cursor.execute(
                    """UPDATE centros_productivos SET esquemas_ids = %s
                    WHERE nombre = %s RETURNING centro_id""",
                    (lista_esquemas_ids_nueva, nombre_centro))
                centro_id = cursor.fetchone()[0]

                # Eliminamos el esquema de la tabla esquemas
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

    def obtener_todos_esquemas(self,nombre_centro):
        """Obtiene todos los esquemas del centro productivo seleccionado"""
        try:
            with self._conn.cursor() as cursor:
                # Primero necesitamos obtener el ID del centro productivo
                cursor.execute(
                    """SELECT centro_id FROM centros_productivos WHERE nombre = %s""",
                    (nombre_centro,)
                )
                centro_id_result = cursor.fetchone()

                if not centro_id_result:
                    print(f"Centro productivo no encontrado: {nombre_centro}")
                    return []

                centro_id = centro_id_result[0]

                # Ahora obtenemos los esquemas asociados al centro
                cursor.execute(
                    """SELECT e.esquema_id, e.nombre, e.canales_entrada, e.canales_salida 
                    FROM esquemas e
                    JOIN centros_productivos cp ON e.esquema_id = ANY(cp.esquemas_ids)
                    WHERE cp.centro_id = %s
                    ORDER BY e.nombre""",
                    (centro_id,)
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

