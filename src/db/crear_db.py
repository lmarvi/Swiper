from .conexion_db import ConexionDB
from src.config.conexion_db_config import DB_CONFIG

dbname = DB_CONFIG["dbname"]

class CrearDB:

    @staticmethod
    def crear_db_si_no_existe():

        conn = ConexionDB(autocommit=True)
        conn.dbname = "postgres"
        conn.conectar()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (dbname,)
                )
                exists = cursor.fetchone()
                if not exists:
                    print("Creando database...")
                    cursor.execute(f'CREATE DATABASE "{dbname}";')
                    print(f"Base de datos {dbname} creada")
                else:
                    print("La base de datos ya existe")
        except Exception as e:
            print(f"Error en la creación de la db: {e}")
            return None

        # Ahora conectamos a la DB y creamos tablas
        conn = ConexionDB(autocommit=True)
        conn.conectar()

        try:
            with conn.cursor() as cursor:
                # Tabla usuarios
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.usuarios (
                        usuario_id     BIGSERIAL PRIMARY KEY,
                        nombre         VARCHAR(50) NOT NULL,
                        contrasena     VARCHAR(50) NOT NULL,
                        rol            CHAR(10)    NOT NULL,
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW(),
                        UNIQUE(nombre)
                    );
                """)
                print("Tabla usuarios creada o ya existente")

                # Tabla esquemas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.esquemas (
                        esquema_id     BIGSERIAL PRIMARY KEY,
                        nombre         VARCHAR(25) NOT NULL,
                        canales_entrada INTEGER[]  NOT NULL,
                        canales_salida  INTEGER[]  NOT NULL,
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW(),
                        UNIQUE(nombre)
                    );
                """)
                print("Tabla esquemas creada o ya existente")

                # Tabla centros_productivos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.centros_productivos (
                        centro_id      BIGSERIAL PRIMARY KEY,
                        nombre         VARCHAR(25) NOT NULL,
                        esquemas_ids   INTEGER[]  NOT NULL,
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW(),
                        UNIQUE(nombre)
                    );
                """)
                print("Tabla centros_productivos creada o ya existente")

                # Tabla accesos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.accesos (
                        acceso_id   BIGSERIAL PRIMARY KEY,
                        usuario_id  BIGINT NOT NULL
                            REFERENCES public.usuarios(usuario_id)
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION,
                        centro_id   BIGINT NOT NULL
                            REFERENCES public.centros_productivos(centro_id)
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION,
                        fecha_creacion TIMESTAMP NOT NULL DEFAULT NOW()
                    );
                """)
                print("Tabla accesos creada o ya existente")

                # Inserción admin si no existe
                cursor.execute("""
                    SELECT 1 FROM public.usuarios WHERE nombre=%s
                """, ("admin",))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO public.usuarios (nombre, contrasena, rol)
                        VALUES (%s, %s, %s)
                    """, ("admin", "swiper", "admin"))
                    print("Usuario admin creado")
                else:
                    print("Usuario admin ya existe")

        finally:
            conn.desconectar()