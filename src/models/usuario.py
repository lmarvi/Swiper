
import datetime


class Usuario:

    def __init__(
        self,
        usuario_id: None,
        nombre_usuario: str,
        contrasena: str,
        rol: str,
        fecha_creacion: None
    ):
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol
        self.fecha_creacion = fecha_creacion if fecha_creacion is not None else datetime.datetime.now()



