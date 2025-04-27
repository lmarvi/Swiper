from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from src.ui.ui import SwiperUI
from src.controllers.main_controller import MainController


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = SwiperUI()
        self.setCentralWidget(self.ui)

        self.setWindowTitle("Swiper")
        self.setGeometry(100, 100, 1500, 850)

        # Instancia del controlador
        self._controller = MainController(self.ui)

        # Icono de la ventana
        logo = QIcon()
        logo.addFile("../img/Logo_final.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(logo)

        # Controlador
        self._controller = MainController(self.ui)

        # Señales
        self.ui.boton_anadir_esquema.clicked.connect(self._controller.anadir_esquema)
        self.ui.boton_editar_esquema.clicked.connect(self._controller.editar_esquema)
        self.ui.boton_eliminar_esquema.clicked.connect(self._controller.eliminar_esquema)