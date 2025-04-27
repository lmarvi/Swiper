from PIL.ImageQt import QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        login_main_layout = QVBoxLayout()
        self.setLayout(login_main_layout)
        self.setGeometry(100,100,400,500)

        logo = QPixmap("../src/img/Logo_final.png")
        logo_escalado = logo.scaled(
            QSize(75, 75),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        logo_label = QLabel()
        logo_label.setPixmap(logo_escalado)
        login_main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)




