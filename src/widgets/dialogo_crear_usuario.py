from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox

from src.models.usuario import Usuario


class UsuarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Usuario")

        self.nombre_edit = QLineEdit()
        self.contrasena_edit = QLineEdit()
        self.rol_edit = QComboBox()
        self.rol_edit.addItems(["USER","ADMIN"])

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Nombre:", self.nombre_edit)
        form_layout.addRow("Contraseña:", self.contrasena_edit)
        form_layout.addRow("Rol:", self.rol_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

    def get_nuevo_usuario(self):
        nuevo_usuario = Usuario(
            usuario_id=None,
            nombre_usuario=self.nombre_edit.text(),
            contrasena=self.contrasena_edit.text(),
            rol=self.rol_edit.currentText(),
            fecha_creacion=None
        )

        return nuevo_usuario