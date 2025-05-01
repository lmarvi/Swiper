from src.db.conexion_db import ConexionDB
from src.models.usuario import Usuario


class UsuarioService:
    def __init__(self,view):
        self.view = view

        self._conn = ConexionDB()
        self._conn.conectar()


    def refrescar_tabla_usuarios(self):
        usuarios = self.obtener_usarios()
        return usuarios


    def crear_usuario(self,nuevo_usuario):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO usuarios (nombre,contrasena,rol) 
                    VALUES (%s,%s,%s) RETURNING usuario_id""",(nuevo_usuario.nombre_usuario,nuevo_usuario.contrasena,nuevo_usuario.rol))
                nuevo_id = cursor.fetchone()[0]
                self._conn.commit()
                return nuevo_id
        except Exception as e:
            print(f"Error en la inserción del usuario: {e}")
            return None

    #def editar_usuario(self,nombre_usuario,contrasena,rol) -> bool:
    #hacer el commit a la db, si no da error QMessagebox usuario editado y actualizar tabla usuarios

    #def eliminar_usuario(self,nombre_usuario):


    def obtener_usarios(self):
        print("obteniendo lista usuarios")

        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM usuarios"
                )
                lista_usuarios = cursor.fetchall()
                print(lista_usuarios)
                if lista_usuarios:
                    return lista_usuarios
                else:
                    return None
        except Exception as e:
            print(f"Error en la consulta de la lista de usuarios: {e}")
            return None

    def cerrar_conexion(self):
        if hasattr(self, '_conn') and self._conn:
            self._conn.desconectar()
            self._conn = None
