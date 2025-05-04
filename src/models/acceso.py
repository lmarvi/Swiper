

class Acceso:
    def __init__(
        self,
        acceso_id: int = None,
        usuario_id: int = None,
        centro_id: int = None,
        fecha_creacion=None
    ):
        self.acceso_id = acceso_id
        self.usuario_id = usuario_id
        self.centro_id = centro_id
        self.fecha_creacion = fecha_creacion or __import__('datetime').datetime.now()

