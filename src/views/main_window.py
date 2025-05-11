from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from src.controllers.acceso_controller import AccesoController
from src.controllers.centro_productivo_controller import CentroController
from src.controllers.usuario_controller import UsuarioController
from src.services.usuario_service import UsuarioService
from src.services.acceso_service import AccesoService
from src.ui.ui import SwiperUI
from src.controllers.main_window_controller import MainWindowController


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.usuario_service = UsuarioService(self)
        self.setWindowTitle("Swiper")
        self.setGeometry(200, 200, 1500, 850)

        # Icono de la ventana
        logo = QIcon()
        logo.addFile("../img/Logo_final.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(logo)

        # Controlador
        self.ui = None
        self._controllerMainWindow = None
        self._controllerUsuario = None
        self._controllerCentro = None
        self._controllerAcceso = None

    def configurar_interfaz(self, esAdmin):

        self.ui = SwiperUI(esAdmin)
        self.setCentralWidget(self.ui)

        # Configurar el controlador
        self._controllerMainWindow = MainWindowController(self.ui)
        self._controllerUsuario = UsuarioController(self.ui)
        self._controllerCentro = CentroController(self.ui)
        self._controllerAcceso = AccesoController(self.ui)

        # Pasar el servicio al controlador
        self._controllerUsuario.UsuarioService = self.usuario_service

        # Conectar señales
        self.ui.boton_anadir_esquema.clicked.connect(self._controllerMainWindow.anadir_esquema)
        self.ui.boton_editar_esquema.clicked.connect(self._controllerMainWindow.editar_esquema)
        self.ui.boton_eliminar_esquema.clicked.connect(self._controllerMainWindow.eliminar_esquema)

        self.ui.boton_anadir_usuario.clicked.connect(self._controllerUsuario.datos_nuevo_usuario)
        self.ui.boton_editar_usuario.clicked.connect(self._controllerUsuario.datos_usuario_editado)
        self.ui.boton_eliminar_usuario.clicked.connect(self._controllerUsuario.id_usuario)

        self.ui.boton_anadir_centro.clicked.connect(self._controllerCentro.datos_nuevo_centro)
        self.ui.boton_editar_centro.clicked.connect(self._controllerCentro.datos_centro_editado)
        self.ui.boton_eliminar_centro.clicked.connect(self._controllerCentro.id_centro)

        self.ui.boton_anadir_acceso.clicked.connect(self._controllerAcceso.datos_nuevo_acceso)
        self.ui.boton_editar_acceso.clicked.connect(self._controllerAcceso.datos_acceso_editado)
        self.ui.boton_eliminar_acceso.clicked.connect(self._controllerAcceso.id_acceso)


    def cerrar_conexion(self, conn):
        # Cierra recursos antes de cerrar la aplicación
        if hasattr(self, 'usuario_service'):
            self.usuario_service.cerrar_conexion()
        # ...
        super().closeEvent(conn)