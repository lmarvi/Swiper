from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox


class EditUsuarioDialog(QDialog):
    def __init__(self, parent=None, usuario_id=None, nombre="", contrasena="", rol=""):
        super().__init__(parent)
        self.usuario_id = usuario_id

        self.setWindowTitle("Editar Usuario")

        self.nombre_edit = QLineEdit(nombre)
        self.contrasena_edit = QLineEdit(contrasena)
        self.rol_edit = QComboBox()
        self.rol_edit.addItems(["USER","ADMIN"])

        index = self.rol_edit.findText(rol)
        if index >= 0:
            self.rol_edit.setCurrentIndex(index)

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


    def get_usuario_editado(self):

        nombre_edit = self.nombre_edit.text()
        contrasena_edit = self.contrasena_edit.text()
        rol_edit = self.rol_edit.currentText()

        usuario_editado = {
            'usuario_id': self.usuario_id,
            'nombre_usuario': nombre_edit if nombre_edit else None,
            'contrasena': contrasena_edit if contrasena_edit else None,
            'rol': rol_edit if rol_edit else None
        }

        return usuario_editado