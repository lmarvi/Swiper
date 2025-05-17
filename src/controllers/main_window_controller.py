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
        self.esquema_service = EsquemaService(view)
        self.esquema_controller = EsquemaController(view)
        # Lista para tener los esquemas ordenados
        self.esquemas_ids = {}
        self.boton_previo = None

    def inicializar_aplicacion(self):
        """Inicializa la aplicación cargando esquemas de la BD"""
        self.esquema_controller.cargar_esquemas(self)
        # Conectar evento de selección de esquema
        self.view.grupo_canales.buttonClicked.connect(self.si_esquema_seleccionado)

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

        self.limpiar_canales()
        # Seleccionamos automáticamente el nuevo esquema
        btn.setChecked(True)

        # Como el esquema no existe en la BD, no tiene ID asociado así que
        # lo marcamos con un ID temporal None
        self.esquemas_ids[texto.strip()] = None

    def editar_esquema(self):
        """Gestiona el estado de los botones según si estamos en modo edición o no"""
        esquema_seleccionado = self.view.grupo_canales.checkedButton()
        if esquema_seleccionado is None:
            self.view.boton_editar_esquema.setChecked(False)
            QMessageBox.warning(self.view,"Error","Selecciona un esquema para editar los colores")
            return

        if self.view.boton_editar_esquema.isChecked():
            # Acabamos de entrar en modo edición:
            # guardamos el esquema actual como “previo” por si se cambia
            self.boton_previo = esquema_seleccionado

        editar_activado = self.view.boton_editar_esquema.isChecked()
        habilitar_botones = esquema_seleccionado and editar_activado

        # Habilito el estado de los botones para poder configurar el esquema
        self.view.boton_anadir_entrada.setEnabled(habilitar_botones)
        self.view.boton_quitar_entrada.setEnabled(habilitar_botones)
        self.view.boton_guardar.setEnabled(habilitar_botones)
        self.habilitar_botones_entrada_mover()
        self.habilitar_botones_salida_mover()

    def eliminar_esquema(self):
        """Elimina el esquema seleccionado"""
        # Crear una instancia del controlador de esquemas si no existe
        if not hasattr(self, 'esquema_controller'):
            from src.controllers.esquema_controller import EsquemaController
            self.esquema_controller = EsquemaController(self.view)

        # Llamar al metodo de eliminar esquema pasando self como el controlador
        self.esquema_controller.esquema_a_eliminar(self)

    def habilitar_boton_guardar(self):
        """Actualiza el estado del boton guardar esquema basado en la selección"""
        hay_seleccion = self.view.grupo_canales.checkedButton() is not None
        modo_edicion = self.view.boton_editar_esquema.isChecked()

        # Verificar si es el primer o último botón
        if hay_seleccion and modo_edicion:
            # Solo habilitar si hay algo seleccionado y el modo edición está activo
            self.view.boton_guardar.setEnabled(hay_seleccion)

    def datos_nuevo_esquema(self):
        datos_esquema = EsquemaController(self.view)
        nuevo_esquema = datos_esquema.get_nuevo_esquema(self)
        if nuevo_esquema:
            esquema_id = self.esquema_service.guardar_esquema(nuevo_esquema)
            if esquema_id:
                # Actualizar el id del esquema en la lista de esquemas
                nombre_esquema = self.view.grupo_canales.checkedButton().text()
                self.esquemas_ids[nombre_esquema] = esquema_id
                QMessageBox.information(self.view, "Información", "Esquema guardado con éxito")
                self.refrescar_canales_esquema_actual()
            else:
                QMessageBox.warning(self.view, "Error", "No se ha podido guardar el esquema")

    def refrescar_canales_esquema_actual(self):
        """Refresca los canales del esquema actualmente seleccionado"""
        btn_seleccionado = self.view.grupo_canales.checkedButton()
        if btn_seleccionado:
            nombre_esquema = btn_seleccionado.text()
            if nombre_esquema in self.esquemas_ids:
                esquema_id = self.esquemas_ids[nombre_esquema]
                if esquema_id:
                    # Limpiar canales actuales
                    self.limpiar_canales()
                    # Recargar desde la base de datos
                    self.esquema_controller.cargar_detalle_esquema(self, esquema_id)

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
        modo_edicion = self.view.boton_editar_esquema.isChecked()

        # Solo habilitar si hay algo seleccionado Y estamos en modo edición
        habilitar = hay_seleccion and modo_edicion

        # Por defecto los botones están deshabilitados
        self.view.boton_subir_entrada.setEnabled(False)
        self.view.boton_bajar_entrada.setEnabled(False)

        # Verificar si es el primer o último botón
        if habilitar:
            seleccionado = self.view.grupo_entrada.checkedButton()
            botones = self.obtener_orden_botones_entrada()
            if botones:
                indice = botones.index(seleccionado)
                # Deshabilitar botón subir si es el primero
                self.view.boton_subir_entrada.setEnabled(indice > 0)
                # Deshabilitar botón bajar si es el último
                self.view.boton_bajar_entrada.setEnabled(indice < len(botones) - 1)

    def habilitar_botones_salida_mover(self):
        """Actualiza el estado de los botones de mover basado en la selección y el modo edición"""
        hay_seleccion = self.view.grupo_salida.checkedButton() is not None
        modo_edicion = self.view.boton_editar_esquema.isChecked()

        # Solo habilitar si hay algo seleccionado Y estamos en modo edición
        habilitar = hay_seleccion and modo_edicion

        # Por defecto los botones están deshabilitados
        self.view.boton_subir_salida.setEnabled(False)
        self.view.boton_bajar_salida.setEnabled(False)

        # Verificar si es el primer o último botón si estamos en modo edición
        if habilitar:
            seleccionado = self.view.grupo_salida.checkedButton()
            botones = self.obtener_orden_botones_salida()
            if botones:
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
        # Metodo para modificar el nombre de un esquema al hacer doble clic en él
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

    def si_esquema_seleccionado(self, boton_nuevo):
        if self.view.boton_editar_esquema.isChecked():
            prev = self.boton_previo or boton_nuevo  # botón antes del cambio
            respuesta = QMessageBox.question(
                self.view,
                "Cambiar de esquema",
                "Se perderán los cambios realizados en este esquema. ¿Desea continuar?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.No:
                # restaurar el anterior y desmarcar el clic nuevo
                self._restaurar_seleccion_esquema(prev, boton_nuevo)
                return
            else:
                # confirmado: salimos de edición y actualizamos previo
                self.view.boton_editar_esquema.setChecked(False)
                self.editar_esquema()

        # cambio válido: limpiar y cargar nuevo
        self.boton_previo = boton_nuevo
        self.limpiar_canales()
        esquema_id = self.esquemas_ids.get(boton_nuevo.text())
        self.esquema_controller.cargar_detalle_esquema(self, esquema_id)

    def _restaurar_seleccion_esquema(self, btn_antiguo,btn_nuevo):
        # para evitar problemas con las señales
        self.view.grupo_canales.blockSignals(True)

        # desmarcar el clic que el usuario acaba de hacer
        btn_nuevo.setChecked(False)
        # y marcar solo el anterior
        if btn_antiguo:
            btn_antiguo.setChecked(True)
        self.view.grupo_canales.blockSignals(False)

    def limpiar_esquemas(self):
        """Limpia todos los esquemas de la interfaz"""
        # Obtener todos los botones en el layout
        botones = []
        layout = self.view.layout_esquemas_draganddrop
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget:
                botones.append(widget)

        # Eliminar cada botón
        for btn in botones:
            self.view.grupo_canales.removeButton(btn)
            layout.removeWidget(btn)
            btn.setParent(None)
            btn.deleteLater()

        # Limpiar el diccionario de referencias
        self.esquemas_ids.clear()

    def anadir_esquema_desde_db(self, nombre, esquema_id):
        """Añade un esquema desde la base de datos a la interfaz"""
        btn = BotonCanal(nombre, "#D9D9D9", parent=self.view)
        btn.dobleClicSignal.connect(self.esquema_doble_clic)
        self.view.layout_esquemas_draganddrop.addWidget(btn)
        self.view.grupo_canales.addButton(btn)

        # Guardar referencia del ID
        self.esquemas_ids[nombre] = esquema_id

    def limpiar_canales(self):
        """Limpia los canales de entrada y salida"""
        # Limpiar entrada
        self._limpiar_layout(self.view.layout_entrada_draganddrop, self.view.grupo_entrada)

        # Limpiar salida
        self._limpiar_layout(self.view.layout_salida_draganddrop, self.view.grupo_salida)

    def _limpiar_layout(self, layout, grupo_botones):
        """Metodo para limpiar el layout"""
        botones = []
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget:
                botones.append(widget)

        for btn in botones:
            grupo_botones.removeButton(btn)
            layout.removeWidget(btn)
            btn.setParent(None)
            btn.deleteLater()

    def cargar_canales_entrada(self, colores):
        """Carga los canales de entrada según la lista proporcionada"""
        if not colores:
            return

        for color in colores:
            # Obtener el color hexadecimal del diccionario COLORES_CONFIG
            if color in COLORES_CONFIG:
                color_hexadecimal = COLORES_CONFIG[color]

                # Crear el botón con el color
                btn = BotonCanal(color, color_hexadecimal, parent=self.view)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.setMinimumWidth(200)
                self.view.layout_entrada_draganddrop.addWidget(btn, alignment=Qt.AlignHCenter)
                self.view.grupo_entrada.addButton(btn)

    def cargar_canales_salida(self, colores):
        """Carga los canales de salida según la lista proporcionada"""
        if not colores:
            return

        for color in colores:
            # Obtener el color hexadecimal del diccionario COLORES_CONFIG
            if color in COLORES_CONFIG:
                color_hexadecimal = COLORES_CONFIG[color]

                # Crear el botón con el color
                btn = BotonCanal(color, color_hexadecimal, parent=self.view)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.setMinimumWidth(200)
                self.view.layout_salida_draganddrop.addWidget(btn, alignment=Qt.AlignHCenter)
                self.view.grupo_salida.addButton(btn)




