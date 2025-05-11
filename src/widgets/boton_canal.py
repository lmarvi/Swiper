from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QSizePolicy


class BotonCanal(QPushButton):
    dobleClicSignal = Signal(QPushButton)

    def __init__(self, texto: str, color: str, parent=None):
        super().__init__(texto, parent)
        # Color base y versión clara
        base = QColor(color)
        claro = base.lighter(100)  # 50% más claro
        self._bg_unselected = claro.name()
        self._bg_selected = base.name()

        # Configuración de tamaño y cursor
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumHeight(30)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)

        # Radio de borde (mitad de la altura)
        self._radius = self.minimumHeight() // 2

        # Stylesheets
        self._unselected = f"""
                    QPushButton {{
                        background-color: {self._bg_unselected};
                        border: none;
                        border-radius: {self._radius}px;
                        color: #212121;
                        padding: 4px 12px;
                    }}
                """
        self._selected = f"""
                    QPushButton {{
                        background-color: {self._bg_selected};
                        border: 2px solid #2196F3;
                        border-radius: {self._radius}px;
                        color: #212121;
                        padding: 4px 12px;
                    }}
                """
        self.setStyleSheet(self._unselected)
        self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked: bool):
        self.setStyleSheet(self._selected if checked else self._unselected)

    def mouseDoubleClickEvent(self, event):
        # Emitimos la señal de doble clic
        self.dobleClicSignal.emit(self)
        super().mouseDoubleClickEvent(event)