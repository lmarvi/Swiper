"""
from .color import Color
from .esquema import Esquema

class Canal:
    def __init__(
        self,
        canal_id: int,
        nombre_canal: str,
        color: Color,
        posicion_entrada: int,
        posicion_salida: int,
        esquema: Esquema
    ):
        self.canal_id = canal_id
        self.nombre_canal = nombre_canal
        self.color = color
        self.posicion_entrada = posicion_entrada
        self.posicion_salida = posicion_salida
        self.esquema = esquema
"""