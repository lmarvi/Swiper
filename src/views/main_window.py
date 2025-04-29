from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from src.ui.ui import SwiperUI
from src.controllers.main_window_controller import MainWindowController


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Swiper")
        self.setGeometry(200, 200, 1500, 850)

        # Icono de la ventana
        logo = QIcon()
        logo.addFile("../img/Logo_final.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(logo)

        # Controlador
        self.ui = None
        self._controller = None

    def configurar_interfaz(self, esAdmin):

        self.ui = SwiperUI(esAdmin)
        self.setCentralWidget(self.ui)

        # Configurar el controlador
        self._controller = MainWindowController(self.ui)

        # Conectar señales
        self.ui.boton_anadir_esquema.clicked.connect(self._controller.anadir_esquema)
        self.ui.boton_editar_esquema.clicked.connect(self._controller.editar_esquema)
        self.ui.boton_eliminar_esquema.clicked.connect(self._controller.eliminar_esquema)