from PySide6.QtWidgets import QMessageBox
from src.db.conexion_db import ConexionDB


class CentroService:
    def __init__(self,view):
        self.view = view

        self._conn = ConexionDB()
        self._conn.conectar()

    def crear_centro(self,nuevo_centro):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                     """INSERT INTO centros_productivos (nombre, esquemas_ids) 
                    VALUES (%s, %s) RETURNING centro_id""",
                    (nuevo_centro.nombre_centro, [])
                )
                nuevo_id = cursor.fetchone()[0]
                self._conn.commit()
                return nuevo_id
        except Exception as e:
            print(f"Error en la inserción del centro: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al crear el centro productivo: {e}"
            )
            return None

    def editar_centro(self, centro_editado):
        try:
            # Obtenemos los datos actuales para comparar
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT nombre FROM centros_productivos WHERE centro_id = %s",
                    (centro_editado['centro_id'],)
                )
                actual = cursor.fetchone()
                if not actual:
                    return False

                if centro_editado['nombre'] is not None:
                    cursor.execute(
                        "UPDATE centros_productivos SET nombre = %s WHERE centro_id = %s RETURNING centro_id",
                        (centro_editado['nombre'], centro_editado['centro_id'])
                    )
                id = cursor.fetchone()[0]
                self._conn.commit()
                return id
        except Exception as e:
            print(f"Error en la edición del centro productivo: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al editar el centro productivo: {e}"
            )
            return None


    def eliminar_centro(self,id):
        id = int(id)

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM centros_productivos WHERE centro_id = %s RETURNING centro_id, nombre",(id,)
                )
                centro_eliminado = cursor.fetchone()

                if centro_eliminado:
                    self._conn.commit()
                    return True
                else:
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        "No se ha encontrado el centro productivo en la base de datos para eliminar"
                    )
                    return False

        except Exception as e:
            print(f"Error eliminando el centro productivo: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al eliminar el centro productivo: {e}"
            )

            return False

    def obtener_centros(self):
        print("obteniendo lista centros")

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM centros_productivos"
                )
                lista_centros = cursor.fetchall()
                print(lista_centros)
                if lista_centros:
                    return lista_centros
                else:
                    return None
        except Exception as e:
            print(f"Error en la consulta de la lista de centros: {e}")
            return None

    def cerrar_conexion(self):
        if hasattr(self, '_conn') and self._conn:
            self._conn.desconectar()
            self._conn = None
