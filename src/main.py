import sys


from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy, \
    QPushButton, QListWidget
from PySide6.QtWidgets import QGraphicsDropShadowEffect


import creardb


class Swiper(QMainWindow):

    def __init__(self):
        # creardb.Crear_db.crear_db_si_no_exite()

        super().__init__()

        self.setWindowTitle("Swiper")
        self.setGeometry(100, 100, 1500, 800)

        # Icono de la ventana
        icon = QIcon()
        icon.addFile("../img/Logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # Widget principal y layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_widget.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.main_widget.setLayout(self.main_layout)

        # Layout superior con logo y título
        self.layout_titulo = QHBoxLayout()
        self.layout_titulo.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.layout_titulo)

        # Logo
        self.frame_logo = QFrame()
        self.frame_logo.setFrameShape(QFrame.NoFrame)
        self.logo_swiper = QLabel()
        self.logo_swiper.setPixmap(QPixmap("../img/Logo.png"))
        self.logo_swiper.setScaledContents(True)
        self.logo_swiper.setFixedSize(75, 75)
        self.frame_logo_layout = QVBoxLayout()
        self.frame_logo_layout.setContentsMargins(25, 0, 0, 0)
        self.frame_logo_layout.addWidget(self.logo_swiper, alignment=Qt.AlignTop)
        self.frame_logo.setLayout(self.frame_logo_layout)
        self.layout_titulo.addWidget(self.frame_logo, alignment=Qt.AlignTop)

        # Contenedor para el título con margen para la sombra
        self.container_titulo = QFrame()
        # El contenedor es más grande para permitir que se vea la sombra
        self.container_titulo.setFixedSize(280, 100)
        self.container_titulo.setStyleSheet("background-color: transparent;")

        container_layout = QVBoxLayout(self.container_titulo)
        container_layout.setContentsMargins(0, 0, 0, 0)  # Margen para que se vea la sombra

        # Frame del título
        self.frame_titulo = QFrame()
        self.frame_titulo.setFixedSize(210, 60)
        self.frame_titulo.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 24px;
                color: #212121;
            }
        """)

        # Configurar efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(4, 4)
        shadow.setColor(Qt.black)
        self.frame_titulo.setGraphicsEffect(shadow)

        # Label del título centrado dentro del frame
        self.label_titulo = QLabel("SWIPER", self.frame_titulo)
        self.label_titulo.setAlignment(Qt.AlignCenter)

        font_titulo = QFont("Segoe UI", 24, QFont.Weight.Bold)
        self.label_titulo.setFont(font_titulo)

        self.titulo_centrado_layout = QVBoxLayout(self.frame_titulo)
        self.titulo_centrado_layout.setContentsMargins(0, 0, 0, 0)
        self.titulo_centrado_layout.addWidget(self.label_titulo, alignment=Qt.AlignCenter)

        # Añadir el frame del título al contenedor
        container_layout.addWidget(self.frame_titulo, alignment=Qt.AlignCenter)

        # Añadir expansores para centrar
        self.layout_titulo.addStretch()


        self.layout_titulo.addWidget(self.container_titulo)
        self.layout_titulo.addStretch()

        self.main_layout.addSpacing(10)

        ####### Layout Botones #######
        self.layout_menu = QHBoxLayout()
        self.layout_menu.setContentsMargins(0, 0, 0, 0)
        self.layout_menu.setSpacing(20)
        self.frame_menu = QFrame()
        self.frame_menu.setFixedHeight(65)
        self.frame_menu.setFrameShape(QFrame.NoFrame)
        self.frame_menu.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                color: #212121;
            }""")
        self.frame_menu.setGraphicsEffect(shadow)

        self.layout_botones_menu = QHBoxLayout(self.frame_menu)
        self.layout_botones_menu.setContentsMargins(0, 0, 0, 0)
        self.layout_botones_menu.setSpacing(0)
        self.layout_menu.addLayout(self.layout_botones_menu)
        self.frame_menu.setLayout(self.layout_botones_menu)
        self.main_layout.addWidget(self.frame_menu)

            ####### Botones #######
        self.frame_menu_interno = QFrame()
        self.frame_menu_interno.setFixedSize(800, 50)
        self.frame_menu_interno.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                color: #212121;
            }""")

        self.layout_interno_botones = QHBoxLayout()
        self.layout_interno_botones.setContentsMargins(10, 10, 10, 10)
        self.layout_interno_botones.setSpacing(100)
        self.layout_interno_botones.setAlignment(Qt.AlignCenter)
        self.frame_menu_interno.setLayout(self.layout_interno_botones)
        self.layout_botones_menu.addWidget(self.frame_menu_interno)

            ###### Botones ######
        self.boton_anadir_esquema = QPushButton("Añadir esquema")
        self.layout_interno_botones.addWidget(self.boton_anadir_esquema, alignment=Qt.AlignCenter)
        self.boton_anadir_esquema.setFixedSize(120,35)
        #self.boton_anadir_esquema.clicked.connect(self.anadir_esquema)

        self.boton_editar_esquema = QPushButton("Editar esquema")
        self.layout_interno_botones.addWidget(self.boton_editar_esquema, alignment=Qt.AlignCenter)
        self.boton_editar_esquema.setFixedSize(120,35)
        #self.boton_editar_esquema.clicked.connect(self.editar_esquema)

        self.boton_eliminar_esquema = QPushButton("Eliminar esquema")
        self.layout_interno_botones.addWidget(self.boton_eliminar_esquema, alignment=Qt.AlignCenter)
        self.boton_eliminar_esquema.setFixedSize(120,35)
        #self.boton_eliminar_esquema.clicked.connect(self.eliminar_esquema)

        self.boton_configuracion = QPushButton("Configuracion")
        self.layout_interno_botones.addWidget(self.boton_configuracion, alignment=Qt.AlignCenter)
        self.boton_configuracion.setFixedSize(120,35)
        #self.boton_configuracion.clicked.connect(self.configurar)

        ####### Layout Canales y Procesado ########

        self.main_horizontal_layout_canales = QHBoxLayout()
        self.main_horizontal_layout_canales.setContentsMargins(0, 0, 0, 20)
        self.main_horizontal_layout_canales.setSpacing(20)
        self.main_layout.addLayout(self.main_horizontal_layout_canales)
        self.frame_blanco_canales = QFrame()
        self.frame_blanco_canales.setFixedHeight(500)
        self.frame_blanco_canales.setFrameShape(QFrame.NoFrame)
        self.frame_blanco_canales.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                color: #212121;
            }""")
        self.frame_blanco_canales.setGraphicsEffect(shadow)

        self.layout_vertical_columnas = QHBoxLayout(self.frame_blanco_canales)
        self.main_horizontal_layout_canales.addLayout(self.layout_vertical_columnas)
        self.frame_blanco_canales.setLayout(self.layout_vertical_columnas)
        self.main_layout.addWidget(self.frame_blanco_canales)

        self.layout_esquemas_contenedor = QVBoxLayout()
        self.layout_entrada_contenedor = QVBoxLayout()
        self.layout_salida_contenedor = QVBoxLayout()
        self.layout_procesado_contenedor = QVBoxLayout()


        self.frame_esquemas_contenedor = QFrame()
        self.frame_esquemas_contenedor.setFixedSize(300, 450)
        self.frame_esquemas_contenedor.setStyleSheet("""
            QFrame {
                background-color: #ebebeb;
                color: #212121;
                border-radius: 24px;
            }""")
        self.frame_esquemas_contenedor.setLayout(self.layout_esquemas_contenedor)
        self.layout_vertical_columnas.addWidget(self.frame_esquemas_contenedor)

        self.frame_entrada_contenedor = QFrame()
        self.frame_entrada_contenedor.setFixedSize(300, 450)
        self.frame_entrada_contenedor.setStyleSheet("""
            QFrame {
                background-color: #ebebeb;
                color: #212121;
                border-radius: 24px;
            }""")
        self.frame_entrada_contenedor.setLayout(self.layout_entrada_contenedor)
        self.layout_vertical_columnas.addWidget(self.frame_entrada_contenedor)

        self.frame_salida_contenedor = QFrame()
        self.frame_salida_contenedor.setFixedSize(300, 450)
        self.frame_salida_contenedor.setStyleSheet("""
            QFrame {
                background-color: #ebebeb;
                color: #212121;
                border-radius: 24px;
            }""")
        self.frame_salida_contenedor.setLayout(self.layout_salida_contenedor)
        self.layout_vertical_columnas.addWidget(self.frame_salida_contenedor)

        self.frame_procesado_contenedor = QFrame()
        self.frame_procesado_contenedor.setFixedSize(300, 450)
        self.frame_procesado_contenedor.setStyleSheet("""
            QFrame {
                background-color: #ebebeb;
                color: #212121;
                border-radius: 24px;
            }""")
        self.frame_procesado_contenedor.setLayout(self.layout_procesado_contenedor)
        self.layout_vertical_columnas.addWidget(self.frame_procesado_contenedor)


        ###### COLUMNA ESQUEMAS ######

        self.label_esquemas = QLabel("ESQUEMAS")
        self.layout_esquemas_contenedor.addWidget(self.label_esquemas)
        self.label_esquemas.setAlignment(Qt.AlignCenter)
        self.label_esquemas.setStyleSheet("color: #333333;")

        self.lista_esquemas = QListWidget()
        self.lista_esquemas.setFixedSize(275,400)
        self.layout_esquemas_contenedor.addWidget(self.lista_esquemas)

        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Swiper()
    window.show()
    sys.exit(app.exec())