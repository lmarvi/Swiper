from PySide6.QtCore import Qt
from PySide6.QtWidgets import QInputDialog, QMessageBox, QComboBox, QDialog, QSizePolicy

from src.config.colores_config import COLORES_CONFIG
from src.controllers.esquema_controller import EsquemaController
from src.services.esquema_service import EsquemaService
from src.widgets.boton_canal import BotonCanal
from src.widgets.dialogo_nuevo_color import NuevoColorDialog


class MainWindowController:
    def __init__(self,view):
        self.view = view
        self.EsquemaService = EsquemaService(view)

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

    def habilitar_boton_guardar(self):
        """Actualiza el estado del boton guardar esquema basado en la selección"""
        hay_seleccion = self.view.grupo_canales.checkedButton() is not None

        # Verificar si es el primer o último botón
        if hay_seleccion:
            # Solo habilitar si hay algo seleccionado
            self.view.boton_guardar.setEnabled(hay_seleccion)

    def datos_nuevo_esquema(self):
        datos_esquema = EsquemaController(self.view)
        nuevo_esquema = datos_esquema.get_nuevo_esquema(self)
        if nuevo_esquema:
            pasar_datos = self.EsquemaService.guardar_esquema(nuevo_esquema)
            if pasar_datos:
                QMessageBox.information(self.view, "Información", "Esquema guardado con éxito")
            else:
                QMessageBox.warning(self.view, "Error", "No se ha podido guardar el esquema")

    def anadir_entrada(self):

        dialog = NuevoColorDialog(None)
        resultado = dialog.exec()

        if resultado == QDialog.Accepted:
            color = dialog.get_color()

            if color:
                color_hexadecimal = COLORES_CONFIG[f"{color}"]

                # Creamos el botón en la entrada
                btn_entrada = BotonCanal(color, color_hexadecimal, parent=self.view)
                btn_entrada.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn_entrada.setMinimumWidth(200)
                self.view.layout_entrada_draganddrop.addWidget(btn_entrada, alignment=Qt.AlignHCenter)
                self.view.grupo_entrada.addButton(btn_entrada)

                # Creamos un duplicado del botón en la salida
                btn_salida = BotonCanal(color, color_hexadecimal, parent=self.view)
                btn_salida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn_salida.setMinimumWidth(200)
                self.view.layout_salida_draganddrop.addWidget(btn_salida, alignment=Qt.AlignHCenter)
                self.view.grupo_salida.addButton(btn_salida)
        else:
            return

    def quitar_entrada(self):
        btn = self.view.grupo_entrada.checkedButton()
        if btn is None:
            return QMessageBox.warning(self.view, "Error", "Ningún color seleccionado")

        resp = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro que deseas eliminar el color '{btn.text()}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resp != QMessageBox.Yes:
            return

        # Quitar el botón del frame y del grupo
        self.view.frame_entrada.removeWidget(btn)
        self.view.grupo_entrada.removeButton(btn)

        # Limpiar el widget
        btn.setParent(None)
        btn.deleteLater()

    def habilitar_botones_entrada_mover(self):
        """Actualiza el estado de los botones de mover basado en la selección"""
        hay_seleccion = self.view.grupo_entrada.checkedButton() is not None
        total_botones = len(self.obtener_orden_botones_entrada())

        # Solo habilitar si hay algo seleccionado
        self.view.boton_subir_entrada.setEnabled(hay_seleccion)
        self.view.boton_bajar_entrada.setEnabled(hay_seleccion)

        # Verificar si es el primer o último botón
        if hay_seleccion:
            seleccionado = self.view.grupo_entrada.checkedButton()
            botones = self.obtener_orden_botones_entrada()
            indice = botones.index(seleccionado)

            # Deshabilitar botón subir si es el primero
            self.view.boton_subir_entrada.setEnabled(indice > 0)

            # Deshabilitar botón bajar si es el último
            self.view.boton_bajar_entrada.setEnabled(indice < len(botones) - 1)

    def habilitar_botones_salida_mover(self):
        """Actualiza el estado de los botones de mover basado en la selección"""
        hay_seleccion = self.view.grupo_salida.checkedButton() is not None
        total_botones = len(self.obtener_orden_botones_salida())

        # Solo habilitar si hay algo seleccionado
        self.view.boton_subir_salida.setEnabled(hay_seleccion)
        self.view.boton_bajar_salida.setEnabled(hay_seleccion)

        # Verificar si es el primer o último botón
        if hay_seleccion:
            seleccionado = self.view.grupo_salida.checkedButton()
            botones = self.obtener_orden_botones_salida()
            indice = botones.index(seleccionado)

            # Deshabilitar botón subir si es el primero
            self.view.boton_subir_salida.setEnabled(indice > 0)

            # Deshabilitar botón bajar si es el último
            self.view.boton_bajar_salida.setEnabled(indice < len(botones) - 1)

    def subir_entrada(self):
        """Mueve el color seleccionado una posición hacia arriba"""
        btn = self.view.grupo_entrada.checkedButton()
        if not btn:
            return

        layout = self.view.layout_entrada_draganddrop
        index = self.obtener_indice_en_layout(layout, btn)

        if index > 0:
            # Quito el botón
            layout.removeWidget(btn)
            # Reinserción una posición arriba
            layout.insertWidget(index - 1, btn, alignment=Qt.AlignCenter)

    def bajar_entrada(self):
        """Mueve el color seleccionado una posición hacia abajo"""
        btn = self.view.grupo_entrada.checkedButton()
        if not btn:
            return

        layout = self.view.layout_entrada_draganddrop
        index = self.obtener_indice_en_layout(layout, btn)
        count = layout.count()

        if index < count - 1:
            # Remover el botón
            layout.removeWidget(btn)
            # Reinsertarlo una posición abajo
            layout.insertWidget(index + 1, btn, alignment=Qt.AlignCenter)

    def subir_salida(self):
        """Mueve el color seleccionado una posición hacia arriba"""
        btn = self.view.grupo_salida.checkedButton()
        if not btn:
            return

        layout = self.view.layout_salida_draganddrop
        index = self.obtener_indice_en_layout(layout, btn)

        if index > 0:
            # Quito el botón
            layout.removeWidget(btn)
            # Reinserción una posición arriba
            layout.insertWidget(index - 1, btn, alignment=Qt.AlignCenter)

    def bajar_salida(self):
        """Mueve el color seleccionado una posición hacia abajo"""
        btn = self.view.grupo_salida.checkedButton()
        if not btn:
            return

        layout = self.view.layout_salida_draganddrop
        index = self.obtener_indice_en_layout(layout, btn)
        count = layout.count()

        if index < count - 1:
            # Remover el botón
            layout.removeWidget(btn)
            # Reinsertarlo una posición abajo
            layout.insertWidget(index + 1, btn, alignment=Qt.AlignCenter)

    def obtener_indice_en_layout(self, layout, widget):
        """Encuentra el índice de un color en un layout"""
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == widget:
                return i
        return -1

    def obtener_orden_botones_entrada(self):
        botones = []
        layout = self.view.layout_entrada_draganddrop
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, BotonCanal):
                botones.append(widget)
        return botones

    def obtener_orden_botones_salida(self):
        botones = []
        layout = self.view.layout_salida_draganddrop
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, BotonCanal):
                botones.append(widget)
        return botones

    def obtener_nombre_orden_botones_entrada(self):
        nombre_colores = []
        layout = self.view.layout_entrada_draganddrop
        for i in range(layout.count()):
            nombre = layout.itemAt(i).widget().text()
            nombre_colores.append(nombre)
        return nombre_colores

    def obtener_nombre_orden_botones_salida(self):
        nombre_colores = []
        layout = self.view.layout_salida_draganddrop
        for i in range(layout.count()):
            nombre = layout.itemAt(i).widget().text()
            nombre_colores.append(nombre)
        return nombre_colores

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




