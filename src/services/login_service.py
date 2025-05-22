from src.db.conexion_db import ConexionDB


class LoginService:
    def __init__(self,view):
        self.view = view

        self._conn = ConexionDB()
        self._conn.conectar()

    def consulta_rol(self, usuario):

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT rol FROM usuarios WHERE nombre = %s",
                    (usuario,)
                )
                rol = cursor.fetchone()
                if rol:
                    return rol[0]
                else:
                    return None
        except Exception as e:
            print(f"Error en la consulta del rol: {e}")
            return None

    def consulta_login(self, usuario, contrasena):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM usuarios WHERE nombre = %s AND contrasena = %s;",
                    (usuario, contrasena)
                )
                exists = cursor.fetchone()
                return exists
        except Exception as e:
            print(f"Error en la consulta del login: {e}")
            return None

    def consulta_usuario_accesos(self, usuario):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT centro_productivo FROM vista_accesos WHERE nombre_usuario = %s;",
                    (usuario,)
                )
                lista_accesos = cursor.fetchall()
                centros = [centro[0] for centro in lista_accesos]
                print("Lista de centros: ",centros)
                return centros if centros else None
        except Exception as e:
            print(f"Error en la consulta de la lista de accesos: {e}")
            return None