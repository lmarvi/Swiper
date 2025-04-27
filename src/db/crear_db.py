from .conexion_db import ConexionDB

DB_NAME     = "swiper"
DB_USER     = "postgres"
DB_PASSWORD = "1234"
DB_HOST     = "localhost"
DB_PORT     = 5432

class CrearDB:

    @staticmethod
    def crear_db_si_no_existe():
        admin_conn = ConexionDB(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
            dbname="postgres", port=DB_PORT, autocommit=True
        ).conectar()

        try:
            with admin_conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,)
                )
                exists = cursor.fetchone()
                if not exists:
                    print("Creando database...")
                    cursor.execute(f'CREATE DATABASE "{DB_NAME}";')
                    print(f"Base de datos {DB_NAME} creada")
                else:
                    print("La base de datos ya existe")
        finally:
            admin_conn.close()

        # Ahora conectamos a la DB y creamos tablas
        app_conn = ConexionDB(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
            dbname=DB_NAME, port=DB_PORT, autocommit=True
        ).conectar()

        try:
            with app_conn.cursor() as cursor:
                # Tabla usuarios
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.usuarios (
                        usuario_id     BIGSERIAL PRIMARY KEY,
                        nombre         VARCHAR(50) NOT NULL,
                        contrasena     VARCHAR(50) NOT NULL,
                        rol            CHAR(10)    NOT NULL,
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW()
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
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW()
                    );
                """)
                print("Tabla esquemas creada o ya existente")

                # Tabla centros_productivos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.centros_productivos (
                        centro_id      BIGSERIAL PRIMARY KEY,
                        nombre         VARCHAR(25) NOT NULL,
                        ip_servidor    VARCHAR(50) NOT NULL,
                        esquemas_ids   INTEGER[]  NOT NULL,
                        fecha_creacion TIMESTAMP   NOT NULL DEFAULT NOW()
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
            app_conn.close()
