from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QFormLayout, QVBoxLayout

from src.models.acceso import Acceso
from src.services.usuario_service import UsuarioService
from src.services.centro_service import CentroService


class NuevoAccesoDialog(QDialog):
    def __init__(self, parent: None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Acceso")

        # Instancias
        self.usuario_service = UsuarioService(self)
        self.centro_service = CentroService(self)

        self.usuario_select = QComboBox()
        lista_usuarios = self.usuario_service.obtener_nombres_usuarios()
        print(f"Debug - Usuarios: {lista_usuarios}")
        self.usuario_select.addItems(lista_usuarios)
        self.centro_productivo_select = QComboBox()
        lista_centros = self.centro_service.obtener_nombres_centros_productivos()
        print(f"Debug - Centros: {lista_centros}")
        self.centro_productivo_select.addItems(lista_centros)

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Usuario", self.usuario_select)
        form_layout.addRow("Centro productivo", self.centro_productivo_select)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

    def get_nuevo_acceso(self):

        nombre_seleccionado = self.usuario_select.currentText()
        centro_seleccionado = self.centro_productivo_select.currentText()


        usuario_id = self.usuario_service.obtener_id_por_nombre(nombre_seleccionado)
        centro_id = self.centro_service.obtener_id_centro_por_nombre(centro_seleccionado)

        nuevo_acceso = Acceso(
            acceso_id=None,
            usuario_id=usuario_id,
            centro_id=centro_id,
            fecha_creacion=None
        )
        return nuevo_acceso

