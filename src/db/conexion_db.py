import psycopg

class ConexionDB:

    # Gestión de la conexión a PostgreSQL.

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        dbname: str,
        port: int,
        autocommit: bool = False
    ):
        self.host       = host
        self.user       = user
        self.password   = password
        self.dbname     = dbname
        self.port       = port
        self.autocommit = autocommit
        self._conn      = None

    def conectar(self):

        self._conn = psycopg.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
            port=self.port,
            autocommit=self.autocommit
        )
        return self._conn

    def desconectar(self):

        if self._conn:
            self._conn.close()
            self._conn = None

    def ejecutar_consulta(self, query: str, params: tuple = ()):

        with self._conn.cursor() as cursor:
            cursor.execute(query, params)
            try:
                return cursor.fetchall()
            except psycopg.ProgrammingError:
                return None
