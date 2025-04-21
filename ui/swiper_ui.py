from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy, \
    QPushButton, QSpacerItem, QGraphicsDropShadowEffect, QInputDialog, QButtonGroup

from widgets.boton_canal import Boton_canal


class SwiperUI(QWidget):

    def __init__(self):
        super().__init__()
        self.grupo_canales = QButtonGroup(self)  # Definir aquí para que sea accesible en toda la clase
        self.grupo_canales.setExclusive(True)
        self.build_ui()

    def build_ui(self):

        main = QVBoxLayout(self)
        main.setContentsMargins(0,0,0,0)
        main.setSpacing(10)

        # Widget principal y layout
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: rgb(235, 235, 235);")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_widget.setLayout(main_layout)
        main.addWidget(main_widget)

        # Layout superior con logo y título
        layout_titulo = QHBoxLayout()
        layout_titulo.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout_titulo)

        # Logo
        frame_logo = QFrame()
        frame_logo.setFrameShape(QFrame.NoFrame)
        logo_swiper = QLabel()
        logo_swiper.setPixmap(QPixmap("../img/Logo.png"))
        logo_swiper.setScaledContents(True)
        logo_swiper.setFixedSize(75, 75)
        frame_logo_layout = QVBoxLayout()
        frame_logo_layout.setContentsMargins(25, 0, 0, 0)
        frame_logo_layout.addWidget(logo_swiper, alignment=Qt.AlignTop)
        frame_logo.setLayout(frame_logo_layout)
        layout_titulo.addWidget(frame_logo, alignment=Qt.AlignTop)

        # Contenedor para el título con margen para la sombra
        container_titulo = QFrame()
        # El contenedor es más grande para permitir que se vea la sombra
        container_titulo.setFixedSize(280, 100)
        container_titulo.setStyleSheet("background-color: transparent;")

        container_layout = QVBoxLayout(container_titulo)
        container_titulo.setFixedSize(210 + 24*2, 60 + 24*2)  # Margen para que se vea la sombra
        container_layout.setContentsMargins(24, 24, 24, 24)

        # Frame del título
        frame_titulo = QFrame()
        frame_titulo.setFixedSize(210, 60)
        frame_titulo.setStyleSheet("""
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
        container_titulo.setGraphicsEffect(shadow)


        # Label del título centrado dentro del frame
        label_titulo = QLabel("SWIPER", frame_titulo)
        label_titulo.setAlignment(Qt.AlignCenter)

        font_titulo = QFont("Segoe UI", 24, QFont.Weight.Bold)
        label_titulo.setFont(font_titulo)

        titulo_centrado_layout = QVBoxLayout(frame_titulo)
        titulo_centrado_layout.setContentsMargins(0, 0, 0, 0)
        titulo_centrado_layout.addWidget(label_titulo, alignment=Qt.AlignCenter)

        # Añadir el frame del título al contenedor
        container_layout.addWidget(frame_titulo, alignment=Qt.AlignCenter)

        # Añadir expansores para centrar
        layout_titulo.addStretch()

        layout_titulo.addWidget(container_titulo)
        layout_titulo.addStretch()

        ####### Layout Botones #######
        frame_menu = QFrame()
        frame_menu.setFixedHeight(65)
        frame_menu.setFrameShape(QFrame.NoFrame)
        frame_menu.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        color: #212121;
                    }""")
        frame_menu.setGraphicsEffect(shadow)

        layout_botones_menu = QHBoxLayout(frame_menu)
        layout_botones_menu.setContentsMargins(0, 0, 0, 0)
        layout_botones_menu.setSpacing(0)
        frame_menu.setLayout(layout_botones_menu)
        main_layout.addWidget(frame_menu)

        ####### Botones #######
        frame_menu_interno = QFrame()
        frame_menu_interno.setFixedSize(800, 50)
        frame_menu_interno.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        color: #212121;
                    }""")

        layout_interno_botones = QHBoxLayout()
        layout_interno_botones.setContentsMargins(10, 10, 10, 10)
        layout_interno_botones.setSpacing(100)
        layout_interno_botones.setAlignment(Qt.AlignCenter)
        frame_menu_interno.setLayout(layout_interno_botones)
        layout_botones_menu.addWidget(frame_menu_interno)

        ###### Botones ######
        boton_anadir_esquema = QPushButton("Añadir esquema")
        layout_interno_botones.addWidget(boton_anadir_esquema, alignment=Qt.AlignCenter)
        boton_anadir_esquema.setFixedSize(120, 30)
        boton_anadir_esquema.clicked.connect(self.anadir_esquema)

        boton_editar_esquema = QPushButton("Editar esquema")
        layout_interno_botones.addWidget(boton_editar_esquema, alignment=Qt.AlignCenter)
        boton_editar_esquema.setFixedSize(120, 30)
        # boton_editar_esquema.clicked.connect(editar_esquema)

        boton_eliminar_esquema = QPushButton("Eliminar esquema")
        layout_interno_botones.addWidget(boton_eliminar_esquema, alignment=Qt.AlignCenter)
        boton_eliminar_esquema.setFixedSize(120, 30)
        # boton_eliminar_esquema.clicked.connect(eliminar_esquema)

        boton_configuracion = QPushButton("Configuracion")
        layout_interno_botones.addWidget(boton_configuracion, alignment=Qt.AlignCenter)
        boton_configuracion.setFixedSize(120, 30)
        # boton_configuracion.clicked.connect(configurar)

        ####### Layout Canales y Procesado ########

        main_layout_canales = QVBoxLayout()
        main_layout_canales.setContentsMargins(0, 0, 0, 20)
        main_layout_canales.setSpacing(0)
        main_layout.addLayout(main_layout_canales)
        frame_blanco_canales = QFrame()
        frame_blanco_canales.setFixedHeight(550)
        frame_blanco_canales.setFrameShape(QFrame.NoFrame)
        frame_blanco_canales.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        color: #212121;
                    }""")
        frame_blanco_canales.setGraphicsEffect(shadow)

        layout_general_canales = QHBoxLayout(frame_blanco_canales)
        main_layout_canales.addLayout(layout_general_canales)
        frame_blanco_canales.setLayout(layout_general_canales)
        main_layout.addWidget(frame_blanco_canales)

        ##### Esquemas #####
        layout_contenedor_esquemas = QHBoxLayout()
        layout_contenedor_esquemas.setSpacing(30)
        layout_general_canales.addLayout(layout_contenedor_esquemas)
        layout_contenedor_entrada = QVBoxLayout()
        layout_contenedor_entrada.setSpacing(30)
        layout_general_canales.addLayout(layout_contenedor_entrada)
        layout_contenedor_salida = QVBoxLayout()
        layout_contenedor_salida.setSpacing(30)
        layout_general_canales.addLayout(layout_contenedor_salida)
        layout_contenedor_procesado = QVBoxLayout()
        layout_contenedor_procesado.setSpacing(30)
        layout_general_canales.addLayout(layout_contenedor_procesado)

        ##### Layouts grupo canales #####
        layout_layouts_esquemas = QVBoxLayout()
        layout_layouts_esquemas.setAlignment(Qt.AlignCenter)
        layout_contenedor_esquemas.addLayout(layout_layouts_esquemas)
        layout_layouts_esquemas.setSpacing(5)

        layout_layouts_entrada = QVBoxLayout()
        layout_layouts_entrada.setAlignment(Qt.AlignCenter)
        layout_contenedor_entrada.addLayout(layout_layouts_entrada)
        layout_layouts_entrada.setSpacing(5)

        layout_layouts_salida = QVBoxLayout()
        layout_layouts_salida.setAlignment(Qt.AlignCenter)
        layout_contenedor_salida.addLayout(layout_layouts_salida)
        layout_layouts_salida.setSpacing(5)

        layout_layouts_procesado = QVBoxLayout()
        layout_layouts_procesado.setAlignment(Qt.AlignCenter)
        layout_contenedor_procesado.addLayout(layout_layouts_procesado)
        layout_layouts_procesado.setSpacing(5)

        ###### COLUMNA ESQUEMAS ######
        label_esquemas = QLabel("Esquemas")
        layout_layouts_esquemas.addWidget(label_esquemas)
        label_esquemas.setAlignment(Qt.AlignCenter)
        label_esquemas.setStyleSheet("color: #828282;")
        self.layout_esquemas_draganddrop = QVBoxLayout()
        self.layout_esquemas_draganddrop.setAlignment(Qt.AlignCenter)
        frame_esquemas_contenedor = QFrame()
        frame_esquemas_contenedor.setFixedSize(300, 450)
        frame_esquemas_contenedor.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border: 2px solid #ebebeb;
                        border-radius: 24px;
                    }""")
        frame_esquemas_contenedor.setLayout(self.layout_esquemas_draganddrop)
        layout_layouts_esquemas.addWidget(frame_esquemas_contenedor)

        boton_guardar = QPushButton("Guardar")
        layout_layouts_esquemas.addWidget(boton_guardar, alignment=Qt.AlignCenter)
        boton_guardar.setFixedSize(120, 30)
        # boton_guardar.clicked.connect(guardar)

        ###### COLUMNA ENTRADA ######
        label_entrada = QLabel("Entrada")
        layout_layouts_entrada.addWidget(label_entrada)
        label_entrada.setAlignment(Qt.AlignCenter)
        label_entrada.setStyleSheet("color: #828282;")
        layout_entrada_draganddrop = QVBoxLayout()
        frame_entrada_contenedor = QFrame()
        frame_entrada_contenedor.setFixedSize(300, 450)
        frame_entrada_contenedor.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border: 2px solid #ebebeb;
                        border-radius: 24px;
                    }""")
        frame_entrada_contenedor.setLayout(layout_entrada_draganddrop)
        layout_layouts_entrada.addWidget(frame_entrada_contenedor)
        boton_anadir = QPushButton("Añadir")
        boton_quitar = QPushButton("Quitar")
        boton_anadir.setFixedSize(120, 30)
        boton_quitar.setFixedSize(120, 30)
        botones_entrada_h = QHBoxLayout()
        botones_entrada_h.setContentsMargins(0, 0, 0, 0)
        botones_entrada_h.setSpacing(10)
        botones_entrada_h.addWidget(boton_anadir)
        botones_entrada_h.addWidget(boton_quitar)
        layout_layouts_entrada.addLayout(botones_entrada_h)
        # boton_anadir.clicked.connect(self.guardar_color)
        # boton_quitar.clicked.connect(self.quitar_color)

        ###### COLUMNA SALIDA ######
        label_salida = QLabel("Salida")
        layout_layouts_salida.addWidget(label_salida)
        label_salida.setAlignment(Qt.AlignCenter)
        label_salida.setStyleSheet("color: #828282;")
        layout_salida_draganddrop = QVBoxLayout()
        frame_salida_contenedor = QFrame()
        frame_salida_contenedor.setFixedSize(300, 450)
        frame_salida_contenedor.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border: 2px solid #ebebeb;
                        border-radius: 24px;
                    }""")
        frame_salida_contenedor.setLayout(layout_salida_draganddrop)
        layout_layouts_salida.addWidget(frame_salida_contenedor)
        layout_layouts_salida.addItem(
            QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        )

        ###### COLUMNA PROCESADO ######
        label_procesado = QLabel("Procesado")
        layout_layouts_procesado.addWidget(label_procesado)
        label_procesado.setAlignment(Qt.AlignCenter)
        label_procesado.setStyleSheet("color: #828282;")
        layout_procesado_draganddrop = QVBoxLayout()
        frame_procesado_contenedor = QFrame()
        frame_procesado_contenedor.setFixedSize(300, 450)
        frame_procesado_contenedor.setStyleSheet("""
                    QFrame {
                                background-color: #FFFFFF;
                                border: 2px solid #ebebeb;
                                border-radius: 24px;
                            }""")
        frame_procesado_contenedor.setLayout(layout_procesado_draganddrop)
        layout_layouts_procesado.addWidget(frame_procesado_contenedor)
        boton_procesar = QPushButton("Procesar")
        boton_quitar_proc = QPushButton("Quitar")
        boton_procesar.setFixedSize(120, 30)
        boton_quitar_proc.setFixedSize(120, 30)
        botones_entrada_h2 = QHBoxLayout()
        botones_entrada_h2.setContentsMargins(0, 0, 0, 0)
        botones_entrada_h2.setSpacing(10)
        botones_entrada_h2.addWidget(boton_procesar)
        botones_entrada_h2.addWidget(boton_quitar_proc)
        layout_layouts_procesado.addLayout(botones_entrada_h2)
        # boton_procesar.clicked.connect(guardar)
        # boton_quitar_proc.clicked.connect(guardar)

        # Grupo para los nuevos esquemas
        self.grupo_canales = QButtonGroup(self)
        self.grupo_canales.setExclusive(True)

        # Layout para los esquemas
        self.layout_canales = QHBoxLayout()
        self.layout_canales.setContentsMargins(0, 0, 0, 0)
        self.layout_canales.setSpacing(20)

        canales = []
        for texto, color in canales:
            btn = Boton_canal(texto, color)
            self.grupo_canales.addButton(btn)
            self.layout_canales.addWidget(btn)


    def anadir_esquema(self):

        texto, ok = QInputDialog.getText(
            self,
            "Añadir esquema",
            "Nombre del esquema:"
        )
        if not ok or not texto.strip():
            return

        btn = Boton_canal(texto.strip(), "#D9D9D9", parent=self)
        self.layout_esquemas_draganddrop.addWidget(btn)
        self.grupo_canales.addButton(btn)