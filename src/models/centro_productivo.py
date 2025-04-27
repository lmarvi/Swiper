"""
from typing import List
import datetime

class CentroProductivo:
    def __init__(
        self,
        centro_id: int,
        nombre_centro: str,
        ip_servidor: str,
        esquemas: List[int] = None,
        fecha_creacion: datetime.datetime = None
    ):
        self.centro_id = centro_id
        self.nombre_centro = nombre_centro
        self.ip_servidor = ip_servidor
        self.esquemas: List[int] = esquemas or []
        self.fecha_creacion = fecha_creacion or datetime.datetime.now()
"""