from PySide6.QtWidgets import QDialog, QComboBox, QLabel, QHBoxLayout, QPushButton, QFormLayout, QVBoxLayout


class NuevoColorDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Color")

        self.color_combo = QComboBox()
        self.color_combo.addItems(["Amarillo","Azul","Beige","Cian","Marron","Naranja","Negro","Rosa","Turquesa","Verde"])

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Selecciona un color:",self.color_combo)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

    def get_color(self):
        color = self.color_combo.currentText()

        return color