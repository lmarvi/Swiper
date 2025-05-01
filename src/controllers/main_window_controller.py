from PySide6.QtWidgets import QInputDialog, QMessageBox, QComboBox, QDialog
from src.widgets.boton_canal import BotonCanal


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
        self.view.layout_esquemas_draganddrop.addWidget(btn)
        self.view.grupo_canales.addButton(btn)

    def editar_esquema(self):
        btn = self.view.grupo_canales.checkedButton()
        if btn is None:
            return


        nuevo_texto, ok = QInputDialog.getText(
            self.view,
            "Editar esquema",
            "Nuevo nombre del esquema:",
            text=btn.text()
        )
        if not ok or not nuevo_texto.strip():
            return

        btn.setText(nuevo_texto.strip())

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
        btn = self.view.grupo_entrada.checkedButton()

        colores_combo = QComboBox()
        colores_combo.addItems(["Amarillo","Azul","Beige","Cian","Naranja","Marron","Rosa","Turquesa","Verde"])
        window = QDialog(colores_combo)
        window.show()




