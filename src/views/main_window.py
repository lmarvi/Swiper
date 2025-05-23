from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from src.config.inicializar_config import inicializar_rutas_config
from src.controllers.acceso_controller import AccesoController
from src.controllers.centro_productivo_controller import CentroController
from src.controllers.esquema_controller import EsquemaController
from src.controllers.procesado_controller import ProcesadoController
from src.controllers.usuario_controller import UsuarioController
from src.services.usuario_service import UsuarioService
from src.controllers.main_window_controller import MainWindowController
from src.ui.main_ui import MainUI


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Swiper")
        self.setGeometry(300, 100, 1400, 850)

        # Icono de la ventana
        logo = QIcon()
        logo.addFile("../img/Logo_final.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(logo)

        # Controlador
        self.ui = None
        self._controller = None
        self._controller_usuario = None
        self._controller_centro = None
        self._controller_acceso = None
        self._controller_esquema = None
        self._controller_procesado = None

        self.usuario_service = UsuarioService(self)

    def configurar_interfaz(self, es_admin, nombre_usuario, nombre_centro):

        self.ui = MainUI(es_admin)
        self.setCentralWidget(self.ui)

        # Configurar el controlador
        self._controller = MainWindowController(self.ui)
        self._controller_usuario = UsuarioController(self.ui)
        self._controller_centro = CentroController(self.ui)
        self._controller_acceso = AccesoController(self.ui)
        self._controller_esquema = EsquemaController(self.ui)
        self._controller_procesado = ProcesadoController(self._controller)

        # Inicializamos la configuración
        self._controller.cargar_configuracion()

        # Pasar el servicio al controlador
        self._controller_usuario.UsuarioService = self.usuario_service

        # Conectamos señales comunes a todos los usuarios


        self.ui.boton_anadir_esquema.clicked.connect(self._controller.anadir_esquema)
        self.ui.boton_editar_esquema.clicked.connect(self._controller.editar_esquema)
        self.ui.boton_eliminar_esquema.clicked.connect(lambda: self._controller.eliminar_esquema(nombre_centro))
        self.ui.boton_configuracion.toggled.connect(self.ui.on_toggle_config)
        self.ui.boton_configuracion.toggled.connect(self._controller.deshabilitar_botones_esquemas)
        self.ui.boton_salir.clicked.connect(self._controller.salir)

        self.ui.boton_editar_esquema.toggled.connect(self._controller.editar_esquema)
        self.ui.boton_guardar.clicked.connect(lambda: self._controller.datos_nuevo_esquema(nombre_centro))

        self.ui.boton_anadir_entrada.clicked.connect(self._controller.anadir_entrada)
        self.ui.boton_quitar_entrada.clicked.connect(self._controller.quitar_entrada)
        self.ui.boton_subir_entrada.clicked.connect(self._controller.subir_entrada)
        self.ui.boton_bajar_entrada.clicked.connect(self._controller.bajar_entrada)

        self.ui.boton_subir_salida.clicked.connect(self._controller.subir_salida)
        self.ui.boton_bajar_salida.clicked.connect(self._controller.bajar_salida)

        self.ui.grupo_entrada.buttonClicked.connect(self._controller.habilitar_botones_entrada_mover)
        self.ui.grupo_salida.buttonClicked.connect(self._controller.habilitar_botones_salida_mover)
        self.ui.grupo_esquemas.buttonClicked.connect(self._controller.habilitar_boton_guardar)

        self.ui.boton_carpeta_salida.clicked.connect(self._controller.seleccionar_carpeta_salida)

        self.ui.boton_anadir_disenos.clicked.connect(self._controller.anadir_disenos)
        self.ui.boton_quitar_disenos.clicked.connect(self._controller.quitar_disenos)
        self.ui.boton_procesar.clicked.connect(self._controller_procesado.iniciar_procesado)

        if es_admin:
            self.ui.boton_anadir_usuario.clicked.connect(self._controller_usuario.datos_nuevo_usuario)
            self.ui.boton_editar_usuario.clicked.connect(self._controller_usuario.datos_usuario_editado)
            self.ui.boton_eliminar_usuario.clicked.connect(self._controller_usuario.eliminar_id_usuario)

            self.ui.boton_anadir_centro.clicked.connect(self._controller_centro.datos_nuevo_centro)
            self.ui.boton_editar_centro.clicked.connect(self._controller_centro.datos_centro_editado)
            self.ui.boton_eliminar_centro.clicked.connect(self._controller_centro.elminar_id_centro)

            self.ui.boton_anadir_acceso.clicked.connect(self._controller_acceso.datos_nuevo_acceso)
            self.ui.boton_editar_acceso.clicked.connect(self._controller_acceso.datos_acceso_editado)
            self.ui.boton_eliminar_acceso.clicked.connect(self._controller_acceso.id_acceso)



        # Inicializar la aplicación cargando datos del centro seleccionado en Login
        self._controller.inicializar_aplicacion(nombre_usuario,nombre_centro)

    def cerrar_conexion(self, conn):
        # Cierra recursos antes de cerrar la aplicación
        if hasattr(self, 'usuario_service'):
            self.usuario_service.cerrar_conexion()
        # ...
        super().closeEvent(conn)