
import datetime


class Usuario:

    def __init__(
        self,
        usuario_id: int,
        nombre_usuario: str,
        contrasena: str,
        rol: str,
        fecha_creacion: datetime.datetime = None
    ):
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol
        self.fecha_creacion = fecha_creacion



