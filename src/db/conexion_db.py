from contextlib import contextmanager

import psycopg2
from src.config.conexion_db_config import DB_CONFIG


class ConexionDB:

    # Gestión de la conexión a PostgreSQL.

    def __init__(self, autocommit: bool = False):
        self.host = DB_CONFIG["host"]
        self.user = DB_CONFIG["user"]
        self.password = DB_CONFIG["password"]
        self.dbname = DB_CONFIG["dbname"]
        self.port = DB_CONFIG["port"]
        self.autocommit = autocommit
        self._conn = None

    def conectar(self):

        self._conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
            port=self.port,
        )
        self._conn.autocommit = self.autocommit
        return self._conn

    def desconectar(self):

        if self._conn:
            self._conn.close()
            self._conn = None

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



    @contextmanager
    def cursor(self):
        if self._conn is None:
            self.conectar()
        cur = self._conn.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def commit(self):
        if self._conn:
            self._conn.commit()

