from PIL.ImageQt import QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, \
    QComboBox
from src.controllers.crear_db_controller import CrearDBController

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(4, 4)
        shadow.setColor(Qt.gray)

        login_main_layout = QVBoxLayout()
        login_main_layout.setContentsMargins(30, 15, 30, 30)
        self.setLayout(login_main_layout)

        logo_layout = QVBoxLayout()
        login_main_layout.addLayout(logo_layout)

        frame_layout = QVBoxLayout()
        frame = QFrame()
        frame.setFixedSize(180, 180)
        frame.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border: 2px solid #ebebeb;
                    border-radius: 24px;
                }""")
        frame.setLayout(frame_layout)
        frame.setGraphicsEffect(shadow)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 10, 30, 30)
        container_layout.addWidget(frame, alignment=Qt.AlignCenter)
        login_main_layout.addWidget(container)

        edits_layout = QVBoxLayout()
        frame_layout.addLayout(edits_layout)
        edits_layout.setContentsMargins(5,10,5,0)


        boton_layout = QVBoxLayout()
        frame_layout.addLayout(boton_layout)

        try:
            logo = QPixmap("../src/img/Logo_final.png")
            logo_escalado = logo.scaled(
                QSize(75, 75),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            logo_label = QLabel()
            logo_label.setPixmap(logo_escalado)
            logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
            logo_layout.setContentsMargins(0, 10, 0, 20)
        except:
            # En caso de error al cargar la imagen
            print("Error al cargar el logo")
            placeholder = QLabel("SWIPER")
            placeholder.setStyleSheet("font-size: 18px; font-weight: bold;")
            logo_layout.addWidget(placeholder, alignment=Qt.AlignCenter)


        self.usuario_edit = QLineEdit()
        self.usuario_edit.setFixedSize(150,30)
        edits_layout.addWidget(self.usuario_edit, alignment=Qt.AlignCenter)
        self.usuario_edit.setPlaceholderText("Usuario")


        self.contrasena_edit = QLineEdit()
        self.contrasena_edit.setEchoMode(QLineEdit.Password)
        self.contrasena_edit.setFixedSize(150, 30)
        edits_layout.addWidget(self.contrasena_edit, alignment=Qt.AlignCenter)
        self.contrasena_edit.setPlaceholderText("Contraseña")

        self.accesos_combobox = QComboBox()
        self.accesos_combobox.setFixedSize(150, 30)
        edits_layout.addWidget(self.accesos_combobox)

        self.boton_login = QPushButton("Login")
        boton_layout.addWidget(self.boton_login, alignment=Qt.AlignCenter)





