from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout


class EditCentroDialog(QDialog):
    def __init__(self, parent=None, centro_id=None, nombre=""):
        super().__init__(parent)
        self.centro_id = centro_id

        self.setWindowTitle("Editar Centro Productivo")

        self.nombre_edit = QLineEdit(nombre)

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Nombre Centro Productivo:", self.nombre_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)


    def get_centro_editado(self):

        nombre_edit = self.nombre_edit.text()

        centro_editado = {
            'centro_id': self.centro_id,
            'nombre': nombre_edit if nombre_edit else None,
        }

        return centro_editado