from PySide6.QtWidgets import QMessageBox

from src.db.conexion_db import ConexionDB
from src.models.acceso import Acceso


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
                    VALUES (%s,%s) RETURNING acceso_id""",
                    (nuevo_acceso.usuario_id, nuevo_acceso.centro_id))
                acceso_id = cursor.fetchone()[0]
                self._conn.commit()
                return acceso_id
        except Exception as e:
            print(f"Error en la inserción del usuario: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al crear el usuario: {e}"
            )
            return None

    def editar_acceso(self, acceso_editado):
        try:
            # Verifico si el acceso existe
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT usuario_id, centro_id FROM accesos WHERE acceso_id = %s",
                    (acceso_editado.acceso_id,)
                )
                actual = cursor.fetchone()
                if not actual:
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        "El acceso que intentas editar no existe"
                    )
                    return False

                # Verifico si el nuevo acceso ya existe (excepto el que estamos editando)
                if self.acceso_existe(acceso_editado.usuario_id, acceso_editado.centro_id, acceso_editado.acceso_id):
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        "Ya existe un acceso para este usuario y centro productivo"
                    )
                    return False
                # Si no existe se hace el update
                cursor.execute(
                    """UPDATE accesos SET usuario_id = %s, centro_id = %s 
                    WHERE acceso_id = %s RETURNING acceso_id""",
                    (acceso_editado.usuario_id, acceso_editado.centro_id, acceso_editado.acceso_id)
                )
                acceso_id = cursor.fetchone()[0]
                self._conn.commit()
                return acceso_id

        except Exception as e:
            print(f"Error en la edición del acceso: {e}")
            self._conn.rollback()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Ha ocurrido un error al editar el acceso: {e}"
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
                    "SELECT * FROM vista_accesos"
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

    def obtener_acceso_por_id(self, acceso_id):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT acceso_id, usuario_id, centro_id, fecha_creacion FROM accesos WHERE acceso_id = %s",
                    (acceso_id,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    return Acceso(
                        acceso_id=resultado[0],
                        usuario_id=resultado[1],
                        centro_id=resultado[2],
                        fecha_creacion=resultado[3]
                    )
                else:
                    return None
        except Exception as e:
            print(f"Error obteniendo acceso por ID: {e}")
            return None

    def acceso_existe(self, usuario_id, centro_id, excluir_acceso_id=None):
        """
        Verifica si ya existe un acceso para un usuario y centro específicos
        :param usuario_id: ID del usuario
        :param centro_id: ID del centro productivo
        :param excluir_acceso_id: ID del acceso a excluir de la búsqueda (para el caso de edición)
        :return: True si existe, False si no
        """
        try:
            with self._conn.cursor() as cursor:
                if excluir_acceso_id:
                    cursor.execute(
                        """SELECT 1 FROM accesos 
                        WHERE usuario_id = %s AND centro_id = %s AND acceso_id != %s""",
                        (usuario_id, centro_id, excluir_acceso_id)
                    )
                else:
                    cursor.execute(
                        """SELECT 1 FROM accesos 
                        WHERE usuario_id = %s AND centro_id = %s""",
                        (usuario_id, centro_id)
                    )
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error verificando si el acceso existe: {e}")
            return False

    def cerrar_conexion(self):
        if hasattr(self, '_conn') and self._conn:
            self._conn.desconectar()
            self._conn = None

