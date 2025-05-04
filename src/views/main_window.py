from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from src.controllers.usuario_controller import UsuarioController
from src.services.usuario_service import UsuarioService
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

    def configurar_interfaz(self, esAdmin):

        self.ui = SwiperUI(esAdmin)
        self.setCentralWidget(self.ui)

        # Configurar el controlador
        self._controllerMainWindow = MainWindowController(self.ui)
        self._controllerUsuario = UsuarioController(self.ui)

        # Pasar el servicio al controlador
        self._controllerUsuario.UsuarioService = self.usuario_service

        # Conectar señales
        self.ui.boton_anadir_esquema.clicked.connect(self._controllerMainWindow.anadir_esquema)
        self.ui.boton_editar_esquema.clicked.connect(self._controllerMainWindow.editar_esquema)
        self.ui.boton_eliminar_esquema.clicked.connect(self._controllerMainWindow.eliminar_esquema)

        self.ui.boton_anadir_usuario.clicked.connect(self._controllerUsuario.datos_nuevo_usuario)
        self.ui.boton_editar_usuario.clicked.connect(self._controllerUsuario.datos_usuario_editado)
        self.ui.boton_eliminar_usuario.clicked.connect(self._controllerUsuario.id_usuario)

    def cerrar_conexion(self, conn):
        # Cierra recursos antes de cerrar la aplicación
        if hasattr(self, 'usuario_service'):
            self.usuario_service.cerrar_conexion()
        # ...
        super().closeEvent(conn)