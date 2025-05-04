from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy, \
    QPushButton, QSpacerItem, QGraphicsDropShadowEffect, QInputDialog, QButtonGroup, QLineEdit, QTableWidget, \
    QTableWidgetItem

from src.services.acceso_service import AccesoService
from src.services.centro_service import CentroService
from src.services.usuario_service import UsuarioService
from src.widgets.boton_canal import BotonCanal


class SwiperUI(QWidget):

    def __init__(self,esAdmin):
        super().__init__()
        self.grupo_canales = QButtonGroup(self)  # Definir aquí para que sea accesible en toda la clase
        self.grupo_canales.setExclusive(True)

        self.build_ui(esAdmin)

    def build_ui(self,esAdmin):

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

        main = QVBoxLayout(self)
        main.setContentsMargins(0,0,0,20)
        main.setSpacing(10)

        # Widget principal y layout
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: rgb(235, 235, 235);")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        main_widget.setLayout(self.main_layout)
        main.addWidget(main_widget)

        self.frame_configuracion = self._crear_frame_config(esAdmin)
        self.frame_canales = self._crear_frame_canales()
        main.addWidget(self.frame_canales)
        main.addWidget(self.frame_configuracion)
        self.frame_configuracion.hide()

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
        layout_botones_menu.setContentsMargins(0, 0, 0, 0)
        layout_botones_menu.setSpacing(0)
        frame_menu.setLayout(layout_botones_menu)
        self.main_layout.addWidget(frame_menu)

        ####### Layout Botones #######
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
        self.boton_anadir_esquema = QPushButton("Añadir esquema")
        layout_interno_botones.addWidget(self.boton_anadir_esquema, alignment=Qt.AlignCenter)
        self.boton_anadir_esquema.setFixedSize(120, 30)

        self.boton_editar_esquema = QPushButton("Editar esquema")
        layout_interno_botones.addWidget(self.boton_editar_esquema, alignment=Qt.AlignCenter)
        self.boton_editar_esquema.setFixedSize(120, 30)

        self.boton_eliminar_esquema = QPushButton("Eliminar esquema")
        layout_interno_botones.addWidget(self.boton_eliminar_esquema, alignment=Qt.AlignCenter)
        self.boton_eliminar_esquema.setFixedSize(120, 30)

        self.boton_configuracion = QPushButton("Configuración")
        layout_interno_botones.addWidget(self.boton_configuracion, alignment=Qt.AlignCenter)
        self.boton_configuracion.setFixedSize(120, 30)
        self.boton_configuracion.setCheckable(True)
        self.boton_configuracion.toggled.connect(self._on_toggle_config)

    def _crear_frame_config(self,esAdmin):
        main_layout_configuracion = QVBoxLayout()
        main_layout_configuracion.setContentsMargins(0, 0, 0, 30)
        main_layout_configuracion.setSpacing(0)
        self.main_layout.addLayout(main_layout_configuracion)
        frame_blanco_configuracion = QFrame()
        frame_blanco_configuracion.setFixedHeight(550)
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

    def _crear_frame_canales(self):
        main_layout_canales = QVBoxLayout()
        main_layout_canales.setContentsMargins(0, 0, 0, 30)
        main_layout_canales.setSpacing(0)
        self.main_layout.addLayout(main_layout_canales)
        frame_blanco_canales = QFrame()
        frame_blanco_canales.setFixedHeight(550)
        frame_blanco_canales.setFrameShape(QFrame.NoFrame)
        frame_blanco_canales.setStyleSheet("""
                                QFrame {
                                    background-color: #FFFFFF;
                                    color: #212121;
                                }""")
        frame_blanco_canales.setGraphicsEffect(self.shadow_canales)

        layout_general_canales = QHBoxLayout(frame_blanco_canales)
        main_layout_canales.addLayout(layout_general_canales)
        frame_blanco_canales.setLayout(layout_general_canales)
        self.main_layout.addWidget(frame_blanco_canales)

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

        self.boton_guardar = QPushButton("Guardar")
        layout_layouts_esquemas.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)
        self.boton_guardar.setFixedSize(120, 30)
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
        self.boton_anadir_entrada = QPushButton("Añadir")
        self.boton_quitar_entrada = QPushButton("Quitar")
        self.boton_anadir_entrada.setFixedSize(120, 30)
        self.boton_quitar_entrada.setFixedSize(120, 30)
        botones_entrada_h = QHBoxLayout()
        botones_entrada_h.setContentsMargins(0, 0, 0, 0)
        botones_entrada_h.setSpacing(10)
        botones_entrada_h.addWidget(self.boton_anadir_entrada)
        botones_entrada_h.addWidget(self.boton_quitar_entrada)
        layout_layouts_entrada.addLayout(botones_entrada_h)
        # self.boton_anadir.clicked.connect(self.guardar_color)
        # self.boton_quitar.clicked.connect(self.quitar_color)

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
        self.boton_procesar = QPushButton("Procesar")
        self.boton_quitar_proc = QPushButton("Quitar")
        self.boton_procesar.setFixedSize(120, 30)
        self.boton_quitar_proc.setFixedSize(120, 30)
        botones_entrada_h2 = QHBoxLayout()
        botones_entrada_h2.setContentsMargins(0, 0, 0, 0)
        botones_entrada_h2.setSpacing(10)
        botones_entrada_h2.addWidget(self.boton_procesar)
        botones_entrada_h2.addWidget(self.boton_quitar_proc)
        layout_layouts_procesado.addLayout(botones_entrada_h2)


        # Layout para los esquemas
        self.layout_canales = QHBoxLayout()
        self.layout_canales.setContentsMargins(0, 0, 0, 0)
        self.layout_canales.setSpacing(20)

        canales = []
        for texto, color in canales:
            btn = BotonCanal(texto, color)
            self.grupo_canales.addButton(btn)
            self.layout_canales.addWidget(btn)

        return frame_blanco_canales

    def _on_toggle_config(self, checked: bool):
        if checked:
            self.frame_canales.hide()
            self.frame_configuracion.show()
        else:
            self.frame_configuracion.hide()
            self.frame_canales.show()

    def _frame_config_admin(self):

        config_layout = QHBoxLayout()
        self.layout_general_configuracion.addLayout(config_layout)

        # Primera columna: ajustes básicos

        primera_columna_layout = QVBoxLayout()
        config_layout.addLayout(primera_columna_layout)

        ip_label = QLabel("IP Servidor:")
        primera_columna_layout.addWidget(ip_label)
        ip_label.setContentsMargins(5,0,0,0)

        self.ip_text = QLineEdit()
        primera_columna_layout.addWidget(self.ip_text)
        self.ip_text.setFixedSize(200,30)
        self.ip_text.setEnabled(False)

        ruta_salida_label = QLabel("Carpeta de salida:")
        primera_columna_layout.addWidget(ruta_salida_label)
        self.ruta_salida_text = QLineEdit()
        primera_columna_layout.addWidget(self.ruta_salida_text)
        self.ruta_salida_text.setEnabled(False)
        self.ruta_salida_text.setFixedSize(250,30)

        self.boton_carpeta_salida = QPushButton("Carpeta de salida")
        primera_columna_layout.addWidget(self.boton_carpeta_salida)
        self.boton_carpeta_salida.setFixedSize(120, 30)

        # Segunda columna: tabla de usuarios
        segunda_columna_layout = QVBoxLayout()
        config_layout.addLayout(segunda_columna_layout)

        label_usuarios = QLabel("Usuarios")
        label_usuarios.setAlignment(Qt.AlignCenter)
        label_usuarios.setStyleSheet("font-weight: bold; color: #212121;")
        segunda_columna_layout.addWidget(label_usuarios)

        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(5)
        cabecera = ["id", "Nombre", "Contraseña", "Rol", "Fecha creacion usuario"]
        self.tabla_usuarios.setHorizontalHeaderLabels(cabecera)
        self.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setAlternatingRowColors(True)

        segunda_columna_layout.addWidget(self.tabla_usuarios)
        self.cargar_datos_usuarios()

        layout_botones_usuarios = QHBoxLayout()
        segunda_columna_layout.addLayout(layout_botones_usuarios)

        self.boton_anadir_usuario = QPushButton("Añadir usuario")
        self.boton_editar_usuario = QPushButton("Editar usuario")
        self.boton_eliminar_usuario = QPushButton("Eliminar usuario")
        layout_botones_usuarios.addWidget(self.boton_anadir_usuario)
        layout_botones_usuarios.addWidget(self.boton_editar_usuario)
        layout_botones_usuarios.addWidget(self.boton_eliminar_usuario)
        self.boton_anadir_usuario.setFixedSize(120,30)
        self.boton_editar_usuario.setFixedSize(120, 30)
        self.boton_eliminar_usuario.setFixedSize(120, 30)

        # Layout para centros productivos y accesos:

        layout_centros_accesos = QHBoxLayout()
        segunda_columna_layout.addLayout(layout_centros_accesos)

        layout_centros = QVBoxLayout()
        layout_accesos = QVBoxLayout()
        layout_centros_accesos.addLayout(layout_centros)
        layout_centros_accesos.addLayout(layout_accesos)

        # Tabla centros

        label_centros = QLabel("Centros")
        label_centros.setAlignment(Qt.AlignCenter)
        label_centros.setStyleSheet("font-weight: bold; color: #212121;")
        layout_centros.addWidget(label_centros)

        self.tabla_centros = QTableWidget()
        self.tabla_centros.setColumnCount(4)
        cabecera = ["id", "Nombre Centro Productivo","Esquemas Centro Productivo","Fecha creación centro"]
        self.tabla_centros.setHorizontalHeaderLabels(cabecera)
        self.tabla_centros.horizontalHeader().setStretchLastSection(True)
        self.tabla_centros.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_centros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_centros.setAlternatingRowColors(True)
        layout_centros.addWidget(self.tabla_centros)
        self.cargar_datos_centros()

        layout_botones_centros = QHBoxLayout()
        layout_centros.addLayout(layout_botones_centros)

        self.boton_anadir_centro = QPushButton("Añadir centro")
        self.boton_editar_centro = QPushButton("Editar centro")
        self.boton_eliminar_centro = QPushButton("Eliminar centro")
        layout_botones_centros.addWidget(self.boton_anadir_centro)
        layout_botones_centros.addWidget(self.boton_editar_centro)
        layout_botones_centros.addWidget(self.boton_eliminar_centro)
        self.boton_anadir_centro.setFixedSize(120, 30)
        self.boton_editar_centro.setFixedSize(120, 30)
        self.boton_eliminar_centro.setFixedSize(120, 30)

        # Tabla accesos
        label_accesos = QLabel("Accesos")
        label_accesos.setAlignment(Qt.AlignCenter)
        label_accesos.setStyleSheet("font-weight: bold; color: #212121;")
        layout_accesos.addWidget(label_accesos)

        self.tabla_accesos = QTableWidget()
        self.tabla_accesos.setColumnCount(4)
        cabecera = ["id", "Nombre Usuario", "Acceso", "Fecha creación acceso"]
        self.tabla_accesos.setHorizontalHeaderLabels(cabecera)
        self.tabla_accesos.horizontalHeader().setStretchLastSection(True)
        self.tabla_accesos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_accesos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_accesos.setAlternatingRowColors(True)
        layout_accesos.addWidget(self.tabla_accesos)

        layout_botones_accesos = QHBoxLayout()
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



    def _frame_config(self):

        config_layout = QVBoxLayout()
        self.layout_general_configuracion.addLayout(config_layout)

        ip_label = QLabel("IP Servidor:")
        config_layout.addWidget(ip_label)
        ip_label.setContentsMargins(5, 0, 0, 0)

        self.ip_text = QLineEdit()
        config_layout.addWidget(self.ip_text)
        self.ip_text.setFixedSize(200, 30)
        self.ip_text.setEnabled(False)

        ruta_salida_label = QLabel("Carpeta de salida:")
        config_layout.addWidget(ruta_salida_label)
        self.ruta_salida_text = QLineEdit()
        config_layout.addWidget(self.ruta_salida_text)
        self.ruta_salida_text.setEnabled(False)
        self.ruta_salida_text.setFixedSize(250, 30)

        self.boton_carpeta_salida = QPushButton("Carpeta de salida")
        config_layout.addWidget(self.boton_carpeta_salida)
        self.boton_carpeta_salida.setFixedSize(120, 30)

    def cargar_usuarios(self, lista_usuarios):

        self.tabla_usuarios.setRowCount(len(lista_usuarios))
        for fila, usuario in enumerate(lista_usuarios):
            for col, valor in enumerate(usuario):
                item = QTableWidgetItem(str(valor))
                self.tabla_usuarios.setItem(fila, col, item)

    def cargar_datos_usuarios(self):
        try:
            usuario_service = UsuarioService(self)
            lista_usuarios = usuario_service.obtener_usarios()

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

