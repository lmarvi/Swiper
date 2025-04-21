import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication
import creardb
from ui.swiper_ui import SwiperUI


class MainWindow(QMainWindow):

    def __init__(self):

        # creardb.Crear_db.crear_db_si_no_exite()

        super().__init__()

        self.setWindowTitle("Swiper")
        self.setGeometry(100, 100, 1500, 850)
        self.setCentralWidget(SwiperUI())

        # Icono de la ventana
        logo = QIcon()
        logo.addFile("../img/Logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(logo)






        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())