from PySide6.QtCore import Qt
from PySide6.QtWidgets import QInputDialog, QMessageBox, QComboBox, QDialog

from src.config.colores_config import COLORES_CONFIG
from src.widgets.boton_canal import BotonCanal
from src.widgets.dialogo_nuevo_color import NuevoColorDialog


class MainWindowController:
    def __init__(self,view):
        self.view = view


    def anadir_esquema(self):

        texto, ok = QInputDialog.getText(
            self.view,
            "Añadir esquema",
            "Nombre del esquema:"
        )
        if not ok or not texto.strip():
            return

        btn = BotonCanal(texto.strip(), "#D9D9D9", parent=self.view)
        btn.dobleClicSignal.connect(self.esquema_doble_clic)
        self.view.layout_esquemas_draganddrop.addWidget(btn)
        self.view.grupo_canales.addButton(btn)

    def editar_esquema(self):
        esquema_seleccionado = self.view.grupo_canales.checkedButton()
        if esquema_seleccionado is None:
            self.view.boton_editar_esquema.setChecked(False)
            QMessageBox.warning(self.view,"Error","Selecciona un esquema para editar los colores")
            return
        editar_activado = self.view.boton_editar_esquema.isChecked()
        habilitar_botones = esquema_seleccionado and editar_activado

        # Habilito el estado de los botones para poder configurar el esquema
        self.view.boton_anadir_entrada.setEnabled(habilitar_botones)
        self.view.boton_quitar_entrada.setEnabled(habilitar_botones)


    def eliminar_esquema(self):
        btn = self.view.grupo_canales.checkedButton()
        if btn is None:
            return QMessageBox.warning(self.view,"Error","Ningún esquema seleccionado")
        resp = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro que deseas eliminar el esquema “{btn.text()}”?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resp != QMessageBox.Yes:
            return
        self.view.grupo_canales.removeButton(btn)
        self.view.layout_esquemas_draganddrop.removeWidget(btn)

        btn.setParent(None)
        btn.deleteLater()

    def anadir_entrada(self):

        dialog = NuevoColorDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            color = dialog.get_color()

            if color:
                color_hexadecimal = COLORES_CONFIG[f"{color}"]
                btn = BotonCanal(color,color_hexadecimal,parent=self.view)
                self.view.layout_entrada_draganddrop.addWidget(btn,alignment=Qt.AlignCenter)
                self.view.grupo_entrada.addButton(btn)
        else:
            return





    def quitar_entrada(self):
        btn = self.view.grupo_entrada.checkedButton()

        colores_combo = QComboBox()
        colores_combo.addItems(["Amarillo","Azul","Beige","Cian","Naranja","Marron","Rosa","Turquesa","Verde"])
        window = QDialog(colores_combo)
        window.show()

    def esquema_doble_clic(self, boton):
        # Método para modificar el nombre de un esquema al hacer doble clic en él
        if not self.view.boton_editar_esquema.isChecked():
            return  # No hacer nada si el botón editar no está activado

        # Selecciona automáticamente el botón al hacer doble clic
        boton.setChecked(True)

        # Mostrar el diálogo de edición
        nuevo_texto, ok = QInputDialog.getText(
            self.view,
            "Editar esquema",
            "Nuevo nombre del esquema:",
            text=boton.text()
        )
        if ok and nuevo_texto.strip():
            boton.setText(nuevo_texto.strip())




