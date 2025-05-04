from PySide6.QtWidgets import QDialog, QComboBox, QHBoxLayout, QPushButton, QFormLayout, QVBoxLayout, QLineEdit

from src.models.centro_productivo import CentroProductivo


class NuevoCentroDialog(QDialog):
    def __init__(self, parent: None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Centro Productivo")

        self.nombre_centro_edit = QLineEdit()

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Nombre Centro Productivo", self.nombre_centro_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

    def get_nuevo_centro(self):
        nuevo_centro = CentroProductivo(
            centro_id=None,
            nombre_centro=self.nombre_centro_edit.text(),
            esquemas=None,
            fecha_creacion=None
        )

        return nuevo_centro