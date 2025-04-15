import psycopg

DB_NAME = "swiper"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = 5432

class Crear_db:

    @staticmethod
    def crear_db_si_no_exite():
        try:
            with psycopg.connect(
                dbname="postgres",
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
                    exists = cursor.fetchone()
                    if not exists:
                        print("Creando database")
                        cursor.execute(f'CREATE DATABASE "{DB_NAME}";')
                        print(f"Database {DB_NAME} creada")

                    else:
                        print("Ya existe la database")


                with psycopg.connect(
                        dbname="swiper",
                        user=DB_USER,
                        password=DB_PASSWORD,
                        host=DB_HOST,
                        port=DB_PORT,
                        autocommit=True
                ) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""CREATE TABLE public.usuarios
                                            (
                                                usuario_id bigserial NOT NULL,
                                                nombre character varying(50) NOT NULL,
                                                contrasena character varying(50) NOT NULL,
                                                tipo_usuario character(10) NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                PRIMARY KEY (usuario_id)
                                            );""")
                        print("Tabla usuarios creada")

                        cursor.execute("""CREATE TABLE public.esquemas
                                            (
                                                esquema_id bigserial NOT NULL,
                                                nombre character varying(25) NOT NULL,
                                                canales_entrada character[] NOT NULL,
                                                canales_salida character[] NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                PRIMARY KEY (esquema_id)
                                            );""")
                        print("Tabla esquemas creada")

                        cursor.execute("""CREATE TABLE public.centros_productivos
                                            (
                                                centro_id bigserial NOT NULL,
                                                nombre character varying(25) NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                esquema_id bigint NOT NULL,
                                                PRIMARY KEY (centro_id),
                                                CONSTRAINT esquema_id FOREIGN KEY (esquema_id)
                                                    REFERENCES public.esquemas (esquema_id) MATCH SIMPLE
                                                    ON UPDATE CASCADE
                                                    ON DELETE CASCADE
                                                    NOT VALID
                                            );""")
                        print("Tabla centros_productivos creada")

                        cursor.execute("""CREATE TABLE public.accesos
                                        (
                                            acceso_id bigserial NOT NULL,
                                            usuario_id bigint NOT NULL,
                                            centro_id bigint NOT NULL,
                                            PRIMARY KEY (acceso_id),
                                            CONSTRAINT usuario_id FOREIGN KEY (usuario_id)
                                                REFERENCES public.usuarios (usuario_id) MATCH SIMPLE
                                                ON UPDATE NO ACTION
                                                ON DELETE NO ACTION
                                                NOT VALID,
                                            CONSTRAINT centro_id FOREIGN KEY (centro_id)
                                                REFERENCES public.centros_productivos (centro_id) MATCH SIMPLE
                                                ON UPDATE NO ACTION
                                                ON DELETE NO ACTION
                                                NOT VALID
                                        );""")
                        print("Tabla accesos creada")

                        cursor.execute(f"""INSERT INTO public.usuarios
                                            (nombre,contrasena,tipo_usuario) VALUES (%s, %s, %s);
                                        """, ("admin", "swiper", "admin"))
                        print("Usuario admin creado")

        except Exception as e:
            print("Error al crear/verificar la database:",e)