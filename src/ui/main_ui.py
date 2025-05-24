from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy, \
    QPushButton, QGraphicsDropShadowEffect, QButtonGroup, QLineEdit, QTableWidget, \
    QTableWidgetItem, QListWidget, QSpacerItem

from src.services.acceso_service import AccesoService
from src.services.centro_service import CentroService
from src.services.usuario_service import UsuarioService



class MainUI(QWidget):

    def __init__(self,esAdmin):
        super().__init__()


        # Definir aquí para que sea accesible en toda la clase
        self.grupo_esquemas = QButtonGroup(self)
        self.grupo_esquemas.setExclusive(True)
        self.grupo_entrada = QButtonGroup(self)
        self.grupo_entrada.setExclusive(True)
        self.grupo_salida = QButtonGroup(self)
        self.grupo_salida.setExclusive(True)

        # Configurar efecto de sombra
        self.shadow_titulo = QGraphicsDropShadowEffect()
        self.shadow_titulo.setBlurRadius(20)
        self.shadow_titulo.setOffset(4, 4)
        self.shadow_titulo.setColor(Qt.gray)
        self.shadow_menu = QGraphicsDropShadowEffect()
        self.shadow_menu.setBlurRadius(10)
        self.shadow_menu.setOffset(2, 2)
        self.shadow_menu.setColor(Qt.gray)
        self.shadow_canales = QGraphicsDropShadowEffect()
        self.shadow_canales.setBlurRadius(10)
        self.shadow_canales.setOffset(2, 2)
        self.shadow_canales.setColor(Qt.gray)
        self.shadow_conf = QGraphicsDropShadowEffect()
        self.shadow_conf.setBlurRadius(10)
        self.shadow_conf.setOffset(2, 2)
        self.shadow_conf.setColor(Qt.gray)

        # Widget principal y layout
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: rgb(235, 235, 235);")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Layout superior con logo y título
        layout_titulo = QHBoxLayout()
        layout_titulo.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(layout_titulo)

        # Logo
        frame_logo = QFrame()
        frame_logo.setFrameShape(QFrame.NoFrame)
        logo_swiper = QLabel()
        logo_swiper.setPixmap(QPixmap("../src/img/Logo_final.png"))
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
        frame_titulo.setGraphicsEffect(self.shadow_titulo)


        # Label del título centrado dentro del frame
        label_titulo = QLabel("SWIPER", frame_titulo)
        label_titulo.setAlignment(Qt.AlignCenter)

        font_titulo = QFont("Segoe UI", 24, QFont.Weight.Bold)
        label_titulo.setFont(font_titulo)

        titulo_centrado_layout = QVBoxLayout(frame_titulo)
        titulo_centrado_layout.setContentsMargins(0, 0, 0, 0)
        titulo_centrado_layout.addWidget(label_titulo, alignment=Qt.AlignCenter)

        # Frame del título al contenedor
        container_layout.addWidget(frame_titulo, alignment=Qt.AlignCenter)

        # Expansores para centrar
        layout_titulo.addStretch()

        layout_titulo.addWidget(container_titulo)
        layout_titulo.addStretch()

        spacer = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_layout.addItem(spacer)

        ####### Layout Botones #######
        frame_menu = QFrame()
        frame_menu.setFixedHeight(65)
        frame_menu.setFrameShape(QFrame.NoFrame)
        frame_menu.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        color: #212121;
                    }""")
        frame_menu.setGraphicsEffect(self.shadow_menu)

        layout_botones_menu = QHBoxLayout(frame_menu)
        frame_menu.setLayout(layout_botones_menu)
        self.main_layout.addWidget(frame_menu)

        ####### Layout Botones #######
        frame_menu_interno = QFrame()
        frame_menu_interno.setFixedSize(1450, 50)
        frame_menu_interno.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        color: #212121;
                    }""")

        layout_interno_botones = QHBoxLayout()
        layout_interno_botones.setContentsMargins(10, 10, 10, 10)
        layout_interno_botones.setSpacing(40)
        layout_interno_botones.setAlignment(Qt.AlignCenter)
        frame_menu_interno.setLayout(layout_interno_botones)
        layout_botones_menu.addWidget(frame_menu_interno)

        ###### Botones ######
        self.boton_anadir_esquema = QPushButton("Añadir esquema")
        layout_interno_botones.addWidget(self.boton_anadir_esquema, alignment=Qt.AlignCenter)
        self.boton_anadir_esquema.setFixedSize(120, 30)

        self.boton_editar_esquema = QPushButton("Editar esquema")
        layout_interno_botones.addWidget(self.boton_editar_esquema, alignment=Qt.AlignCenter)
        self.boton_editar_esquema.setFixedSize(120, 30)
        self.boton_editar_esquema.setCheckable(True)

        self.boton_eliminar_esquema = QPushButton("Eliminar esquema")
        layout_interno_botones.addWidget(self.boton_eliminar_esquema, alignment=Qt.AlignCenter)
        self.boton_eliminar_esquema.setFixedSize(120, 30)

        self.boton_configuracion = QPushButton("Configuración")
        layout_interno_botones.addWidget(self.boton_configuracion, alignment=Qt.AlignCenter)
        self.boton_configuracion.setFixedSize(120, 30)
        self.boton_configuracion.setCheckable(True)

        self.label_usuario = QLabel("Usuario:")
        layout_interno_botones.addWidget(self.label_usuario, alignment=Qt.AlignCenter)

        self.text_usuario = QLineEdit()
        layout_interno_botones.addWidget(self.text_usuario, alignment=Qt.AlignCenter)
        self.text_usuario.setEnabled(False)

        self.label_centro = QLabel("Centro Productivo:")
        layout_interno_botones.addWidget(self.label_centro, alignment=Qt.AlignCenter)

        self.text_centro = QLineEdit()
        layout_interno_botones.addWidget(self.text_centro, alignment=Qt.AlignCenter)
        self.text_centro.setEnabled(False)

        self.boton_salir = QPushButton("Salir")
        layout_interno_botones.addWidget(self.boton_salir, alignment=Qt.AlignCenter)
        self.boton_salir.setFixedSize(120, 30)

        self.frame_configuracion = self._crear_frame_config(esAdmin)
        self.frame_principal = self._crear_frame_principal()
        self.main_layout.addWidget(self.frame_principal)
        self.main_layout.addWidget(self.frame_configuracion)
        self.frame_configuracion.hide()

    def _crear_frame_config(self,esAdmin):
        main_layout_configuracion = QVBoxLayout()
        main_layout_configuracion.setContentsMargins(0, 0, 0, 30)
        main_layout_configuracion.setSpacing(0)
        self.main_layout.addLayout(main_layout_configuracion)
        frame_blanco_configuracion = QFrame()
        frame_blanco_configuracion.setFixedHeight(620)
        frame_blanco_configuracion.setFrameShape(QFrame.NoFrame)
        frame_blanco_configuracion.setStyleSheet("""
                                            QFrame {
                                                background-color: #FFFFFF;
                                                color: #212121;
                                            }""")
        frame_blanco_configuracion.setGraphicsEffect(self.shadow_conf)

        self.layout_general_configuracion = QHBoxLayout(frame_blanco_configuracion)
        main_layout_configuracion.addLayout(self.layout_general_configuracion)
        frame_blanco_configuracion.setLayout(self.layout_general_configuracion)
        self.main_layout.addWidget(frame_blanco_configuracion)

        if esAdmin:
            self._frame_config_admin()
        else:
            self._frame_config()

        return frame_blanco_configuracion

    def _crear_frame_principal(self):
        main_layout_canales = QVBoxLayout()
        main_layout_canales.setContentsMargins(0, 0, 0, 0)
        main_layout_canales.setSpacing(0)
        self.main_layout.addLayout(main_layout_canales)
        frame_blanco_canales = QFrame()
        frame_blanco_canales.setFixedHeight(620)
        frame_blanco_canales.setFrameShape(QFrame.NoFrame)
        frame_blanco_canales.setStyleSheet("""
                                QFrame {
                                    background-color: #FFFFFF;
                                    color: #212121;
                                }""")
        frame_blanco_canales.setGraphicsEffect(self.shadow_canales)

        layout_general_canales = QHBoxLayout(frame_blanco_canales)
        layout_general_canales.setSpacing(20)
        layout_general_canales.setContentsMargins(20,10,20,10)
        main_layout_canales.addLayout(layout_general_canales)
        frame_blanco_canales.setLayout(layout_general_canales)
        self.main_layout.addWidget(frame_blanco_canales)

        ##### Esquemas #####
        layout_contenedor_esquemas = QHBoxLayout()
        layout_contenedor_esquemas.setSpacing(0)
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
        self.layout_esquemas_draganddrop.setContentsMargins(10, 25, 10, 10)
        self.layout_esquemas_draganddrop.setSpacing(5)
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

        self.boton_guardar = QPushButton("Guardar Esquema")
        self.boton_guardar.setEnabled(False)
        layout_layouts_esquemas.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)
        self.boton_guardar.setFixedSize(120, 30)


        ###### COLUMNA ENTRADA ######
        label_entrada = QLabel("Entrada")
        layout_layouts_entrada.addWidget(label_entrada)
        label_entrada.setAlignment(Qt.AlignCenter)
        label_entrada.setStyleSheet("color: #828282;")
        self.layout_entrada_draganddrop = QVBoxLayout()
        self.layout_entrada_draganddrop.setContentsMargins(10, 25, 10, 10)
        self.layout_entrada_draganddrop.setSpacing(10)
        self.layout_entrada_draganddrop.setAlignment(Qt.AlignTop)
        frame_entrada_contenedor = QFrame()
        frame_entrada_contenedor.setFixedSize(300, 450)
        frame_entrada_contenedor.setStyleSheet("""
                                QFrame {
                                    background-color: #FFFFFF;
                                    border: 2px solid #ebebeb;
                                    border-radius: 24px;
                                }""")
        frame_entrada_contenedor.setLayout(self.layout_entrada_draganddrop)
        layout_layouts_entrada.addWidget(frame_entrada_contenedor)
        self.boton_anadir_entrada = QPushButton("Añadir")
        self.boton_quitar_entrada = QPushButton("Quitar")
        self.boton_subir_entrada = QPushButton("Subir")
        self.boton_bajar_entrada = QPushButton("Bajar")
        self.boton_anadir_entrada.setFixedSize(60, 30)
        self.boton_quitar_entrada.setFixedSize(60, 30)
        self.boton_subir_entrada.setFixedSize(60, 30)
        self.boton_bajar_entrada.setFixedSize(60, 30)
        self.boton_anadir_entrada.setEnabled(False)
        self.boton_quitar_entrada.setEnabled(False)
        self.boton_subir_entrada.setEnabled(False)
        self.boton_bajar_entrada.setEnabled(False)
        botones_entrada_h = QHBoxLayout()
        botones_entrada_h.setContentsMargins(0, 0, 0, 0)
        botones_entrada_h.setSpacing(10)
        botones_entrada_h.addWidget(self.boton_anadir_entrada)
        botones_entrada_h.addWidget(self.boton_quitar_entrada)
        botones_entrada_h.addWidget(self.boton_subir_entrada)
        botones_entrada_h.addWidget(self.boton_bajar_entrada)
        layout_layouts_entrada.addLayout(botones_entrada_h)


        ###### COLUMNA SALIDA ######
        label_salida = QLabel("Salida")
        layout_layouts_salida.addWidget(label_salida)
        label_salida.setAlignment(Qt.AlignCenter)
        label_salida.setStyleSheet("color: #828282;")
        self.layout_salida_draganddrop = QVBoxLayout()
        self.layout_salida_draganddrop.setContentsMargins(10, 25, 10, 10)
        self.layout_salida_draganddrop.setSpacing(10)
        self.layout_salida_draganddrop.setAlignment(Qt.AlignTop)
        frame_salida_contenedor = QFrame()
        frame_salida_contenedor.setFixedSize(300, 450)
        frame_salida_contenedor.setStyleSheet("""
                                QFrame {
                                    background-color: #FFFFFF;
                                    border: 2px solid #ebebeb;
                                    border-radius: 24px;
                                }""")
        frame_salida_contenedor.setLayout(self.layout_salida_draganddrop)
        layout_layouts_salida.addWidget(frame_salida_contenedor)
        self.boton_subir_salida = QPushButton("Subir")
        self.boton_bajar_salida = QPushButton("Bajar")
        self.boton_subir_salida.setFixedSize(120, 30)
        self.boton_bajar_salida.setFixedSize(120, 30)
        self.boton_subir_salida.setEnabled(False)
        self.boton_bajar_salida.setEnabled(False)
        botones_salida_h = QHBoxLayout()
        botones_salida_h.setContentsMargins(0, 0, 0, 0)
        botones_salida_h.setSpacing(10)
        botones_salida_h.addWidget(self.boton_subir_salida)
        botones_salida_h.addWidget(self.boton_bajar_salida)
        layout_layouts_salida.addLayout(botones_salida_h)


        ###### COLUMNA PROCESADO ######
        label_procesado = QLabel("Procesado")
        layout_layouts_procesado.addWidget(label_procesado)
        label_procesado.setAlignment(Qt.AlignCenter)
        label_procesado.setStyleSheet("color: #828282;")

        contenedor_lista = QFrame()
        contenedor_lista_layout = QVBoxLayout(contenedor_lista)
        contenedor_lista_layout.setContentsMargins(0,0,0,0)
        contenedor_lista.setStyleSheet("background: transparent; border: none;")

        layout_procesado_draganddrop = QVBoxLayout()
        layout_procesado_draganddrop.setContentsMargins(10, 25, 10, 10)
        layout_procesado_draganddrop.setAlignment(Qt.AlignCenter)

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

        self.lista_disenos = QListWidget()
        self.lista_disenos.setStyleSheet("""
            QListWidget {
                border: none;  
                background-color: transparent;  
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 8px;
                margin-bottom: 2px;
            }
            QListWidget::item:selected {
                background-color: #e6e6e6;
                color: #212121;
            }
        """)
        self.lista_disenos.setFixedHeight(425)
        self.lista_disenos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        contenedor_lista_layout.addWidget(self.lista_disenos)
        layout_procesado_draganddrop.addWidget(contenedor_lista)

        self.boton_anadir_disenos = QPushButton("Añadir")
        self.boton_quitar_disenos = QPushButton("Quitar")
        self.boton_procesar = QPushButton("Procesar")
        self.boton_anadir_disenos.setFixedSize(80, 30)
        self.boton_procesar.setFixedSize(80, 30)
        self.boton_quitar_disenos.setFixedSize(80, 30)
        self.boton_anadir_disenos.setEnabled(False)
        self.boton_procesar.setEnabled(False)
        self.boton_quitar_disenos.setEnabled(False)
        botones_procesado_h2 = QHBoxLayout()
        botones_procesado_h2.setContentsMargins(0, 0, 0, 0)
        botones_procesado_h2.setSpacing(10)
        botones_procesado_h2.addWidget(self.boton_anadir_disenos)
        botones_procesado_h2.addWidget(self.boton_quitar_disenos)
        botones_procesado_h2.addWidget(self.boton_procesar)
        layout_layouts_procesado.addLayout(botones_procesado_h2)

        return frame_blanco_canales

    def on_toggle_config(self, checked: bool):
        if checked:
            self.frame_principal.hide()
            self.frame_configuracion.show()
        else:
            self.frame_configuracion.hide()
            self.frame_principal.show()

    def _frame_config_admin(self):

        config_layout_principal = QHBoxLayout()
        config_layout_principal.setContentsMargins(10, 10, 10, 10)
        config_layout_principal.setSpacing(10)
        self.layout_general_configuracion.addLayout(config_layout_principal)

        # Primera columna: ajustes básicos
        primera_columna_layout = QVBoxLayout()
        primera_columna_layout.setSpacing(15)
        primera_columna_layout.setAlignment(Qt.AlignTop)
        config_layout_principal.addLayout(primera_columna_layout)

        # Frame contenedor para configuración básica
        frame_config_basica = QFrame()
        frame_config_basica.setFixedSize(320, 400)
        frame_config_basica.setStyleSheet("""
                QFrame {
                    background-color: #FAFAFA;
                    border: 1px solid #E0E0E0;
                    border-radius: 16px;
                }
            """)

        primera_columna_layout.addWidget(frame_config_basica)

        # Layout interno del frame de configuración
        layout_interno_config = QVBoxLayout(frame_config_basica)
        layout_interno_config.setContentsMargins(20, 20, 20, 20)
        layout_interno_config.setSpacing(20)

        # Título de la sección
        titulo_config = QLabel("Configuración del Sistema")
        titulo_config.setAlignment(Qt.AlignCenter)
        titulo_config.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 16px;
                    padding: 6px;
                    background-color: #F0F0F0;
                    color: #212121;;
                    border-radius: 8px;
                    margin-bottom: 5px;
                    min-height: 20px;
                    max-height: 20px;
                }
            """)
        layout_interno_config.addWidget(titulo_config)

        # IP Servidor
        ip_label = QLabel("IP Servidor:")
        ip_label.setStyleSheet("""
                    QLabel {
                        font-weight: 600;
                        color: #424242;
                        margin-bottom: 5px;
                        background: transparent;
                        border: none;
                    }
                """)
        layout_interno_config.addWidget(ip_label)

        self.ip_text = QLineEdit()
        self.ip_text.setFixedSize(280, 35)
        self.ip_text.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: #212121;
                }
                QLineEdit:focus {
                    border-color: #888888;
                }
                QLineEdit:disabled {
                    background-color: #F5F5F5;
                    color: #9E9E9E;
                }
            """)
        self.ip_text.setEnabled(False)
        layout_interno_config.addWidget(self.ip_text)

        # Carpeta de Salida
        ruta_salida_label = QLabel("Carpeta de salida:")
        ruta_salida_label.setStyleSheet("""
                QLabel {
            font-weight: 600;
            color: #424242;
            margin-bottom: 5px;
            background: transparent;
            border: none;
            }
        """)
        layout_interno_config.addWidget(ruta_salida_label)

        self.ruta_salida_text = QLineEdit()
        self.ruta_salida_text.setEnabled(True)
        self.ruta_salida_text.setReadOnly(True)
        self.ruta_salida_text.setFixedSize(280, 35)
        self.ruta_salida_text.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                    color: #212121;
                }
                QLineEdit:focus {
                    border-color: #888888;
                }
                QLineEdit:disabled {
                    background-color: #F5F5F5;
                    color: #9E9E9E;
                }
            """)
        layout_interno_config.addWidget(self.ruta_salida_text)

        # Botón carpeta de salida
        self.boton_carpeta_salida = QPushButton("Seleccionar Salida")
        self.boton_carpeta_salida.setFixedSize(150, 30)
        self.boton_carpeta_salida.setStyleSheet("""
                QPushButton {
                    background-color: #F0F0F0;
                    border: none;
                    border-radius: 8px;
                    font-size: 12px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #D4D4D4;
                }
                QPushButton:pressed {
                    background-color: #BDBDBD;
                }
            """)
        layout_interno_config.addWidget(self.boton_carpeta_salida)

        # Espaciador
        layout_interno_config.addStretch()

        # Segunda columna: tabla de usuarios
        segunda_columna_layout = QVBoxLayout()
        segunda_columna_layout.setSpacing(15)
        segunda_columna_layout.setAlignment(Qt.AlignTop)
        config_layout_principal.addLayout(segunda_columna_layout)

        # Frame contenedor para usuarios
        frame_usuarios = QFrame()
        frame_usuarios.setFixedSize(1000, 280)
        frame_usuarios.setStyleSheet("""
                QFrame {
                    background-color: #FAFAFA;
                    border: 1px solid #E0E0E0;
                    border-radius: 16px;
                }
            """)

        """ SEGUNDA COLUMNA """
        segunda_columna_layout.addWidget(frame_usuarios)

        # Layout interno usuarios
        layout_usuarios = QVBoxLayout(frame_usuarios)
        layout_usuarios.setContentsMargins(20, 15, 20, 15)
        layout_usuarios.setSpacing(10)

        # Tabla Usuarios
        label_usuarios = QLabel("Usuarios")
        label_usuarios.setAlignment(Qt.AlignCenter)
        label_usuarios.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14px;
                    color: #212121;
                    padding: 6px;
                    background-color: #F0F0F0;
                    border-radius: 8px;
                    margin-bottom: 5px;
                    min-height: 20px;
                    max-height: 20px;
                }
            """)
        layout_usuarios.addWidget(label_usuarios)

        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(5)
        self.tabla_usuarios.setFixedHeight(140)
        cabecera = ["id", "Nombre", "Contraseña", "Rol", "Fecha Creación"]
        self.tabla_usuarios.setHorizontalHeaderLabels(cabecera)
        self.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setAlternatingRowColors(True)
        self.cargar_datos_usuarios()

        # Configurar columnas
        header = self.tabla_usuarios.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 60)
        header.resizeSection(1, 150)
        header.resizeSection(2, 150)
        header.resizeSection(3, 150)

        self.tabla_usuarios.setStyleSheet("""
                QTableWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    selection-background-color: #E8E8E8;
                    alternate-background-color: #FAFAFA;
                }
                QTableWidget::item {
                    padding: 6px;
                    border: none;
                }
                QTableWidget::item:selected {
                    background-color: #E8E8E8;
                    color: #212121;
                }
                QHeaderView::section {
                    background-color: #F5F5F5;
                    color: #424242;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 6px;
                }
            """)
        layout_usuarios.addWidget(self.tabla_usuarios)

        # Botones edición usuarios
        layout_botones_usuarios = QHBoxLayout()
        layout_botones_usuarios.setSpacing(15)
        layout_usuarios.addLayout(layout_botones_usuarios)

        estilo_botones = """
                QPushButton {
                    background-color: #F0F0F0;
                    border: none;
                    border-radius: 8px;
                    font-size: 12px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #D4D4D4;
                }
                QPushButton:pressed {
                    background-color: #BDBDBD;
                }
            """

        self.boton_anadir_usuario = QPushButton("Añadir usuario")
        self.boton_editar_usuario = QPushButton("Editar usuario")
        self.boton_eliminar_usuario = QPushButton("Eliminar usuario")
        layout_botones_usuarios.addWidget(self.boton_anadir_usuario)
        layout_botones_usuarios.addWidget(self.boton_editar_usuario)
        layout_botones_usuarios.addWidget(self.boton_eliminar_usuario)
        self.boton_anadir_usuario.setFixedSize(120,30)
        self.boton_editar_usuario.setFixedSize(120, 30)
        self.boton_eliminar_usuario.setFixedSize(120, 30)
        self.boton_anadir_usuario.setStyleSheet(estilo_botones)
        self.boton_editar_usuario.setStyleSheet(estilo_botones)
        self.boton_eliminar_usuario.setStyleSheet(estilo_botones)

        # Espaciador
        layout_botones_usuarios.addStretch()

        # Centros Productivos y Accesos
        # Frame contenedor
        frame_centros_accesos = QFrame()
        frame_centros_accesos.setFixedSize(1000, 280)
        frame_centros_accesos.setStyleSheet("""
                QFrame {
                    background-color: #FAFAFA;
                    border: 1px solid #E0E0E0;
                    border-radius: 16px;
                }
            """)

        segunda_columna_layout.addWidget(frame_centros_accesos)

        # Layout para centros productivos y accesos:
        layout_centros_accesos = QHBoxLayout(frame_centros_accesos)
        layout_centros_accesos.setContentsMargins(20, 15, 20, 15)
        layout_centros_accesos.setSpacing(25)
        segunda_columna_layout.addLayout(layout_centros_accesos)

        layout_centros = QVBoxLayout()
        layout_accesos = QVBoxLayout()
        layout_centros_accesos.addLayout(layout_centros)
        layout_centros_accesos.addLayout(layout_accesos)
        layout_centros.setSpacing(8)
        layout_accesos.setSpacing(8)

        # Tabla centros
        label_centros = QLabel("Centros Productivos")
        label_centros.setAlignment(Qt.AlignCenter)
        label_centros.setFixedHeight(32)
        label_centros.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14px;
                    color: #212121;
                    padding: 6px;
                    background-color: #F0F0F0;
                    border-radius: 8px;
                    margin-bottom: 5px;
                    min-height: 20px;
                    max-height: 20px;
                }
            """)
        layout_centros.addWidget(label_centros)

        self.tabla_centros = QTableWidget()
        self.tabla_centros.setColumnCount(4)
        self.tabla_centros.setFixedHeight(140)
        self.tabla_centros.setFixedWidth(465)
        cabecera = ["id", "Centro","Esquemas","Fecha Creación"]
        self.tabla_centros.setHorizontalHeaderLabels(cabecera)
        self.tabla_centros.horizontalHeader().setStretchLastSection(True)
        self.tabla_centros.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_centros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_centros.setAlternatingRowColors(True)
        layout_centros.addWidget(self.tabla_centros)
        self.cargar_datos_centros()
        self.tabla_centros.setStyleSheet("""
                QTableWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    selection-background-color: #E8E8E8;
                    alternate-background-color: #FAFAFA;
                }
                QTableWidget::item {
                    padding: 6px;
                    border: none;
                }
                QTableWidget::item:selected {
                    background-color: #E8E8E8;
                    color: #212121;
                }
                QHeaderView::section {
                    background-color: #F5F5F5;
                    color: #424242;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 6px;
                }
            """)

        # Configuración ancho columnas centros
        header_centros = self.tabla_centros.horizontalHeader()
        header_centros.setStretchLastSection(True)
        header_centros.resizeSection(0, 40)
        header_centros.resizeSection(1, 140)
        header_centros.resizeSection(2, 140)


        # Botones Centros
        layout_botones_centros = QHBoxLayout()
        layout_botones_centros.setSpacing(5)
        layout_centros.addLayout(layout_botones_centros)

        self.boton_anadir_centro = QPushButton("Añadir centro")
        self.boton_editar_centro = QPushButton("Editar centro")
        self.boton_eliminar_centro = QPushButton("Eliminar centro")
        layout_botones_centros.addWidget(self.boton_anadir_centro,alignment=Qt.AlignCenter)
        layout_botones_centros.addWidget(self.boton_editar_centro,alignment=Qt.AlignCenter)
        layout_botones_centros.addWidget(self.boton_eliminar_centro,alignment=Qt.AlignCenter)
        self.boton_anadir_centro.setFixedSize(120, 30)
        self.boton_editar_centro.setFixedSize(120, 30)
        self.boton_eliminar_centro.setFixedSize(120, 30)
        self.boton_anadir_centro.setStyleSheet(estilo_botones)
        self.boton_editar_centro.setStyleSheet(estilo_botones)
        self.boton_eliminar_centro.setStyleSheet(estilo_botones)
        layout_botones_centros.addStretch()

        # Tabla accesos
        label_accesos = QLabel("Accesos a Centros Productivos")
        label_accesos.setAlignment(Qt.AlignCenter)
        label_accesos.setFixedHeight(32)
        label_accesos.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14px;
                    color: #212121;
                    padding: 6px;
                    background-color: #F0F0F0;
                    border-radius: 8px;
                    margin-bottom: 5px;
                    min-height: 20px;
                    max-height: 20px;
                }
            """)
        layout_accesos.addWidget(label_accesos)

        self.tabla_accesos = QTableWidget()
        self.tabla_accesos.setColumnCount(4)
        self.tabla_accesos.setFixedHeight(140)
        self.tabla_accesos.setFixedWidth(465)
        cabecera = ["id", "Usuario", "Centro", "Fecha Creación"]
        self.tabla_accesos.setHorizontalHeaderLabels(cabecera)
        self.tabla_accesos.horizontalHeader().setStretchLastSection(True)
        self.tabla_accesos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_accesos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_accesos.setAlternatingRowColors(True)
        layout_accesos.addWidget(self.tabla_accesos)
        self.cargar_datos_accesos()
        self.tabla_accesos.setStyleSheet("""
                QTableWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    selection-background-color: #E8E8E8;
                    alternate-background-color: #FAFAFA;
                }
                QTableWidget::item {
                    padding: 6px;
                    border: none;
                }
                QTableWidget::item:selected {
                    background-color: #E8E8E8;
                    color: #212121;
                }
                QHeaderView::section {
                    background-color: #F5F5F5;
                    color: #424242;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 6px;
                }
            """)

        # Configurar columnas accesos
        header_accesos = self.tabla_accesos.horizontalHeader()
        header_accesos.setStretchLastSection(True)
        header_accesos.resizeSection(0, 40)
        header_accesos.resizeSection(1, 140)
        header_accesos.resizeSection(2, 140)

        # Botones accesos
        layout_botones_accesos = QHBoxLayout()
        layout_botones_accesos.setSpacing(5)
        layout_accesos.addLayout(layout_botones_accesos)

        self.boton_anadir_acceso = QPushButton("Añadir acceso")
        self.boton_editar_acceso = QPushButton("Editar acceso")
        self.boton_eliminar_acceso = QPushButton("Eliminar acceso")
        layout_botones_accesos.addWidget(self.boton_anadir_acceso)
        layout_botones_accesos.addWidget(self.boton_editar_acceso)
        layout_botones_accesos.addWidget(self.boton_eliminar_acceso)
        self.boton_anadir_acceso.setFixedSize(120, 30)
        self.boton_editar_acceso.setFixedSize(120, 30)
        self.boton_eliminar_acceso.setFixedSize(120, 30)
        self.boton_anadir_acceso.setStyleSheet(estilo_botones)
        self.boton_editar_acceso.setStyleSheet(estilo_botones)
        self.boton_eliminar_acceso.setStyleSheet(estilo_botones)
        layout_botones_accesos.addStretch()

    def _frame_config(self):

        # Configuración del Sistema
        config_layout = QVBoxLayout()
        config_layout.setSpacing(15)
        config_layout.setAlignment(Qt.AlignCenter)
        self.layout_general_configuracion.addLayout(config_layout)

        # Frame contenedor para configuración básica
        frame_config_basica = QFrame()
        frame_config_basica.setFixedSize(320, 400)
        frame_config_basica.setStyleSheet("""
                        QFrame {
                            background-color: #FAFAFA;
                            border: 1px solid #E0E0E0;
                            border-radius: 16px;
                        }
                    """)

        config_layout.addWidget(frame_config_basica)

        # Layout interno del frame de configuración
        layout_interno_config = QVBoxLayout(frame_config_basica)
        layout_interno_config.setContentsMargins(20, 20, 20, 20)
        layout_interno_config.setSpacing(20)

        # Título de la sección
        titulo_config = QLabel("Configuración del Sistema")
        titulo_config.setAlignment(Qt.AlignCenter)
        titulo_config.setStyleSheet("""
                        QLabel {
                            font-weight: bold;
                            font-size: 16px;
                            padding: 6px;
                            background-color: #F0F0F0;
                            color: #212121;;
                            border-radius: 8px;
                            margin-bottom: 5px;
                            min-height: 20px;
                            max-height: 20px;
                        }
                    """)
        layout_interno_config.addWidget(titulo_config)

        # IP Servidor
        ip_label = QLabel("IP Servidor:")
        ip_label.setStyleSheet("""
                            QLabel {
                                font-weight: 600;
                                color: #424242;
                                margin-bottom: 5px;
                                background: transparent;
                                border: none;
                            }
                        """)
        layout_interno_config.addWidget(ip_label)

        self.ip_text = QLineEdit()
        self.ip_text.setFixedSize(280, 35)
        self.ip_text.setStyleSheet("""
                        QLineEdit {
                            background-color: #FFFFFF;
                            border: 2px solid #E0E0E0;
                            border-radius: 8px;
                            padding: 8px 12px;
                            font-size: 14px;
                            color: #212121;
                        }
                        QLineEdit:focus {
                            border-color: #888888;
                        }
                        QLineEdit:disabled {
                            background-color: #F5F5F5;
                            color: #9E9E9E;
                        }
                    """)
        self.ip_text.setEnabled(False)
        layout_interno_config.addWidget(self.ip_text)

        # Carpeta de Salida
        ruta_salida_label = QLabel("Carpeta de salida:")
        ruta_salida_label.setStyleSheet("""
                        QLabel {
                    font-weight: 600;
                    color: #424242;
                    margin-bottom: 5px;
                    background: transparent;
                    border: none;
                    }
                """)
        layout_interno_config.addWidget(ruta_salida_label)

        self.ruta_salida_text = QLineEdit()
        self.ruta_salida_text.setEnabled(True)
        self.ruta_salida_text.setReadOnly(True)
        self.ruta_salida_text.setFixedSize(280, 35)
        self.ruta_salida_text.setStyleSheet("""
                        QLineEdit {
                            background-color: #FFFFFF;
                            border: 2px solid #E0E0E0;
                            border-radius: 8px;
                            padding: 8px 12px;
                            font-size: 14px;
                            color: #212121;
                        }
                        QLineEdit:focus {
                            border-color: #888888;
                        }
                        QLineEdit:disabled {
                            background-color: #F5F5F5;
                            color: #9E9E9E;
                        }
                    """)
        layout_interno_config.addWidget(self.ruta_salida_text)

        # Botón carpeta de salida
        self.boton_carpeta_salida = QPushButton("Seleccionar Salida")
        self.boton_carpeta_salida.setFixedSize(150, 30)
        self.boton_carpeta_salida.setStyleSheet("""
                        QPushButton {
                            background-color: #F0F0F0;
                            border: none;
                            border-radius: 8px;
                            font-size: 12px;
                            padding: 8px 16px;
                        }
                        QPushButton:hover {
                            background-color: #D4D4D4;
                        }
                        QPushButton:pressed {
                            background-color: #BDBDBD;
                        }
                    """)
        layout_interno_config.addWidget(self.boton_carpeta_salida)

    def cargar_usuarios(self, lista_usuarios):

        self.tabla_usuarios.setRowCount(len(lista_usuarios))
        for fila, usuario in enumerate(lista_usuarios):
            for col, valor in enumerate(usuario):
                item = QTableWidgetItem(str(valor))
                self.tabla_usuarios.setItem(fila, col, item)

    def cargar_datos_usuarios(self):
        try:
            usuario_service = UsuarioService(self)
            lista_usuarios = usuario_service.obtener_usuarios()

            if lista_usuarios:
                self.cargar_usuarios(lista_usuarios)
            else:
                print("No se encontraron usuarios para mostrar")
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

    def cargar_accesos(self, lista_accesos):
        self.tabla_accesos.setRowCount(len(lista_accesos))
        for fila, usuario in enumerate(lista_accesos):
            for col, valor in enumerate(usuario):
                item = QTableWidgetItem(str(valor))
                self.tabla_accesos.setItem(fila,col,item)

    def cargar_datos_accesos(self):
        try:
            acceso_service = AccesoService(self)
            lista_accesos = acceso_service.obtener_accesos()

            if lista_accesos:
                self.cargar_accesos(lista_accesos)
            else:
                print("No se encontraron accesos para mostrar")
        except Exception as e:
            print(f"Error al cargar accesos: {e}")

    def cargar_centros(self, lista_centros):
        self.tabla_centros.setRowCount(len(lista_centros))
        for fila, centro in enumerate(lista_centros):
            for col, valor in enumerate(centro):
                item = QTableWidgetItem(str(valor))
                self.tabla_centros.setItem(fila, col, item)

    def cargar_datos_centros(self):
        try:
            centro_service = CentroService(self)
            lista_centros = centro_service.obtener_centros()

            if lista_centros:
                self.cargar_centros(lista_centros)
            else:
                print("No se encontraron centros productivos para mostrar")
        except Exception as e:
            print(f"Error al cargar centros: {e}")

