from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QFormLayout, QVBoxLayout

from src.models.acceso import Acceso


class NuevoAccesoDialog(QDialog):
    def __init__(self, parent: None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Acceso")

        self.nombre_select = QComboBox()
        lista_nombres = self.
        self.centro_productivo_select = QComboBox()
        lista_centros = self.
        self.centro_productivo_select.addItems(lista_centros)

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Nombre", self.nombre_select)
        form_layout.addRow("Centro productivo", self.centro_productivo_select)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

    def get_nuevo_acceso(self):
        nuevo_acceso = Acceso(
            acceso_id=None,
            usuario_id=self.nombre_select.currentText(),
            centro_id=self.centro_productivo_select.currentText(),
            fecha_creacion=None
        )

        return nuevo_acceso