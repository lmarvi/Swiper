from src.db.conexion_db import ConexionDB


class UsuarioService:
    def __init__(self,view):
        self.view = view


    def refrescar_tabla_usuarios(self):
        usuarios = self.obtener_usarios()
        return usuarios


    #def crear_usuario(self,nombreUsuario,contrasena,rol) -> bool:
    #    #hacer el commit a la db y devuelve el usuario_id
    #    return usuario_id

    #def editar_usuario(self,nombre_usuario,contrasena,rol) -> bool:
    #hacer el commit a la db, si no da error QMessagebox usuario editado y actualizar tabla usuarios

    #def eliminar_usuario(self,nombre_usuario):

    @staticmethod
    def obtener_usarios():
        print("obteniendo lista usuarios")

        conn = ConexionDB()
        conn.conectar()

        try:
            with conn.cursor() as cursor:
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
