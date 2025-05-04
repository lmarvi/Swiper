from PySide6.QtWidgets import QMessageBox

from src.db.conexion_db import ConexionDB

class AccesoService():
    def __init__(self, view):
        self.view = view

        self._conn = ConexionDB()
        self._conn.conectar()

    def crear_acceso(self, nuevo_acceso):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO accesos (usuario_id,centro_id) 
                    VALUES (%s,%s) RETURNING usuario_id""",
                    (nuevo_usuario.nombre_usuario, nuevo_usuario.contrasena, nuevo_usuario.rol))
                nuevo_id = cursor.fetchone()[0]
                self._conn.commit()
                return nuevo_id
        except Exception as e:
            print(f"Error en la inserción del usuario: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al crear el usuario: {e}"
            )
            return None

    def editar_acceso(self, usuario_editado):
        try:
            # Obtenemos los datos actuales para comparar
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT nombre, contrasena, rol FROM usuarios WHERE usuario_id = %s",
                    (usuario_editado['usuario_id'],)
                )
                actual = cursor.fetchone()
                if not actual:
                    return False

                # Preparamos la consulta SQL
                campos_a_actualizar = []
                valores = []

                if usuario_editado['nombre_usuario'] is not None:
                    campos_a_actualizar.append("nombre = %s")
                    valores.append(usuario_editado['nombre_usuario'])

                if usuario_editado['contrasena'] is not None:
                    campos_a_actualizar.append("contrasena = %s")
                    valores.append(usuario_editado['contrasena'])

                if usuario_editado['rol'] is not None:
                    campos_a_actualizar.append("rol = %s")
                    valores.append(usuario_editado['rol'])

                if not campos_a_actualizar:
                    return True

                # Consulta para actualizar el usuario
                query = f"UPDATE usuarios SET {', '.join(campos_a_actualizar)} WHERE usuario_id = %s RETURNING usuario_id"
                valores.append(usuario_editado['usuario_id'])

                cursor.execute(query, tuple(valores))
                id = cursor.fetchone()[0]
                self._conn.commit()
                return id
        except Exception as e:
            print(f"Error en la edición del usuario: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al editar el usuario: {e}"
            )
            return None

    def eliminar_acceso(self, id):
        id = int(id)

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM accesos WHERE acceso_id = %s RETURNING acceso_id", (id,)
                )
                acceso_eliminado = cursor.fetchone()

                if acceso_eliminado:
                    self._conn.commit()
                    return True
                else:
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        "No se ha encontrado el acceso en la base de datos para eliminar"
                    )
                    return False

        except Exception as e:
            print(f"Error eliminando el acceso: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al eliminar el acceso: {e}"
            )

            return False

    def obtener_accesos(self):
        print("obteniendo lista accesos")

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM accesos"
                )
                lista_accesos = cursor.fetchall()
                print(lista_accesos)
                if lista_accesos:
                    return lista_accesos
                else:
                    return None
        except Exception as e:
            print(f"Error en la consulta de la lista de accesos: {e}")
            return None

    def cerrar_conexion(self):
        if hasattr(self, '_conn') and self._conn:
            self._conn.desconectar()
            self._conn = None

