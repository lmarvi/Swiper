from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox

from src.models.acceso import Acceso
from src.services.acceso_service import AccesoService
from src.services.centro_service import CentroService
from src.services.usuario_service import UsuarioService


class EditAccesoDialog(QDialog):
    def __init__(self, parent=None, acceso_id=None, usuario="",nombre_centro=""):
        super().__init__(parent)
        self.acceso_id = acceso_id

        self.setWindowTitle("Editar Acceso Usuario")

        # Instancias
        self.usuario_service = UsuarioService(self)
        self.centro_service = CentroService(self)
        self.acceso_service = AccesoService(self)

        self.usuario_edit = QComboBox()
        self.centro_edit = QComboBox()
        lista_usuarios = self.usuario_service.obtener_nombres_usuarios()
        lista_centros = self.centro_service.obtener_nombres_centros_productivos()
        self.usuario_edit.addItems(lista_usuarios)
        self.centro_edit.addItems(lista_centros)

        if acceso_id:
            self._cargar_datos_acceso()

        botones = QHBoxLayout()
        self.aceptar_btn = QPushButton("Aceptar")
        self.cancelar_btn = QPushButton("Cancelar")
        botones.addWidget(self.aceptar_btn)
        botones.addWidget(self.cancelar_btn)

        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Usuario:", self.usuario_edit)
        form_layout.addRow("Centro productivo", self.centro_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(botones)

        self.setLayout(main_layout)

    def _cargar_datos_acceso(self):
        #Cargo los datos existentes del acceso en los ComboBox
        try:
            acceso_actual = self.acceso_service.obtener_acceso_por_id(self.acceso_id)

            if acceso_actual:
                # Obtener nombres basados en el id
                nombre_usuario = self.usuario_service.obtener_nombre_por_id(acceso_actual.usuario_id)
                nombre_centro = self.centro_service.obtener_nombre_centro_por_id(acceso_actual.centro_id)

                # Establecer los valores en los ComboBox
                if nombre_usuario:
                    encontrar_usuario = self.usuario_edit.findText(nombre_usuario)
                    if encontrar_usuario >= 0:
                        self.usuario_edit.setCurrentIndex(encontrar_usuario)

                if nombre_centro:
                    encontrar_centro = self.centro_edit.findText(nombre_centro)
                    if encontrar_centro >= 0:
                        self.centro_edit.setCurrentIndex(encontrar_centro)

        except Exception as e:
            print(f"Error cargando datos del acceso: {e}")

    def get_acceso_editado(self):

        usuario_editado = self.usuario_edit.currentText()
        centro_editado = self.centro_edit.currentText()

        usuario_id = self.usuario_service.obtener_id_por_nombre(usuario_editado)
        centro_id = self.centro_service.obtener_id_centro_por_nombre(centro_editado)

        acceso_editado = Acceso(
            acceso_id=self.acceso_id, #id seleccionado
            usuario_id=usuario_id,
            centro_id=centro_id,
            fecha_creacion=None
        )


        return acceso_editado