import sys
from PySide6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.views.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())