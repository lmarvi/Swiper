from PySide6 import QtWidgets,QtGui
import sys,os
from os import listdir
import shutil
import psd_tools
import xml.etree.ElementTree as ET
import psycopg
import psd_tools.compression
import psd_tools.psd
from ui.Swiper_UI import *
from psd_tools.constants import Compression
import tifffile
import ctypes


DB_NAME = "swiper"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = 5432


class Aplicacion(QtWidgets.QMainWindow):


    def crear_db_si_no_exite(self):
        try:
            with psycopg.connect(
                dbname="postgres",
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                autocommit=True
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
                    exists = cursor.fetchone()
                    if not exists:
                        print("Creando database")
                        cursor.execute(f'CREATE DATABASE "{DB_NAME}";')
                        print(f"Database {DB_NAME} creada")

                    else:
                        print("Ya existe la database")


                with psycopg.connect(
                        dbname="swiper",
                        user=DB_USER,
                        password=DB_PASSWORD,
                        host=DB_HOST,
                        port=DB_PORT,
                        autocommit=True
                ) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""CREATE TABLE public.usuarios
                                            (
                                                usuario_id bigserial NOT NULL,
                                                nombre character varying(50) NOT NULL,
                                                contrasena character varying(50) NOT NULL,
                                                tipo_usuario character(10) NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                PRIMARY KEY (usuario_id)
                                            );""")
                        print("Tabla usuarios creada")

                        cursor.execute("""CREATE TABLE public.esquemas
                                            (
                                                esquema_id bigserial NOT NULL,
                                                nombre character varying(25) NOT NULL,
                                                canales character[] NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                PRIMARY KEY (esquema_id)
                                            );""")
                        print("Tabla esquemas creada")

                        cursor.execute("""CREATE TABLE public.centros_productivos
                                            (
                                                centro_id bigserial NOT NULL,
                                                nombre character varying(25) NOT NULL,
                                                fecha_creacion timestamp without time zone NOT NULL DEFAULT NOW(),
                                                esquema_id bigint NOT NULL,
                                                PRIMARY KEY (centro_id),
                                                CONSTRAINT esquema_id FOREIGN KEY (esquema_id)
                                                    REFERENCES public.esquemas (esquema_id) MATCH SIMPLE
                                                    ON UPDATE CASCADE
                                                    ON DELETE CASCADE
                                                    NOT VALID
                                            );""")
                        print("Tabla centros_productivos creada")

                        cursor.execute("""CREATE TABLE public.accesos
                                        (
                                            acceso_id bigserial NOT NULL,
                                            usuario_id bigint NOT NULL,
                                            centro_id bigint NOT NULL,
                                            PRIMARY KEY (acceso_id),
                                            CONSTRAINT usuario_id FOREIGN KEY (usuario_id)
                                                REFERENCES public.usuarios (usuario_id) MATCH SIMPLE
                                                ON UPDATE NO ACTION
                                                ON DELETE NO ACTION
                                                NOT VALID,
                                            CONSTRAINT centro_id FOREIGN KEY (centro_id)
                                                REFERENCES public.centros_productivos (centro_id) MATCH SIMPLE
                                                ON UPDATE NO ACTION
                                                ON DELETE NO ACTION
                                                NOT VALID
                                        );""")
                        print("Tabla accesos creada")

                        cursor.execute(f"""INSERT INTO public.usuarios
                                            (nombre,contrasena,tipo_usuario) VALUES (%s, %s, %s);
                                        """, ("admin", "swiper", "admin"))
                        print("Usuario admin creado")

        except Exception as e:
            print("Error al crear/verificar la database:",e)



    def __init__(self):
        
        # Consulta resolución alto pantalla
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        alto = user32.GetSystemMetrics(1)
        print("El alto de la resolución de pantalla es: ",alto)
        
        super().__init__()
        self.ui = Ui_MainWindow()

        if alto < 1650:
            self.ui.setupUi1080(self)

        else:
            self.ui.setupUi4k(self)

        # Obtener la lista de archivos xml en la carpeta
        self.folder_path = "../XML"
        xmlfiles = [f for f in listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        # Obtener una referencia al objeto list_shemes desde la interfaz de usuario
        self.list_schemes_model = QtGui.QStandardItemModel()
        self.ui.list_schemes.setModel(self.list_schemes_model)
        self.list_designs_model = QtGui.QStandardItemModel()
        self.ui.list_designs.setModel(self.list_designs_model)

        # Mostrar los archivos en el objeto list_schemes_model
        for xmlfile_name in xmlfiles:
            item = QtGui.QStandardItem(xmlfile_name)
            self.list_schemes_model.appendRow(item)
        
        # Conectar la señal clicked del botón bt_add a un método
        self.ui.bt_add.clicked.connect(self.duplicate_file)

        # Conectar la señal clicked del botón bt_del a un método
        self.ui.bt_del.clicked.connect(self.delete_scheme)

        # Conectar la señal clicked del botón bt_edit a un método
        self.ui.bt_edit.clicked.connect(self.open_document)

        # Conectar la señal clicked del botón bt_select a un método
        self.ui.bt_select.clicked.connect(self.select_designs)
        self.selected_designs = []

        # Conectar la señal clicked del botón bt_delFiles a un método
        self.ui.bt_delDesigns.clicked.connect(self.delete_designs)
        
        # Conectar la señal clicked del botón bt_output a un método
        self.ui.bt_output.clicked.connect(self.output_folder)
        
        self.defaultOutputPath = os.path.join(os.path.expanduser("~"), "Desktop")
        self.ui.caja_ruta.setText(self.defaultOutputPath)

        # Conectar la señal clicked del botón bt_proc a un método
        self.ui.bt_proc.clicked.connect(self.process_files)

    #Método para editar los esquemas
    def open_document(self):
        selected_indexes = self.ui.list_schemes.selectedIndexes()

        if selected_indexes:
            row = selected_indexes[0].row()
            item = self.list_schemes_model.item(row)

            file_to_open = os.path.join(self.folder_path, item.text())

            if os.path.exists(file_to_open):
                os.system(f"start {file_to_open}")  # Abre el archivo con la aplicación predeterminada en Windows
                # Puedes adaptar esta línea para otros sistemas operativos

        else:
            print("No se ha seleccionado ningún elemento para editar.")


    #Método para añadir un esquema xml
    def duplicate_file(self):
        
        base_file = os.path.join(self.folder_path, "base.xml")

        # Obtener el nuevo nombre del archivo mediante una ventana emergente
        new_name, ok_pressed = QtWidgets.QInputDialog.getText(self, "Nuevo Nombre", "Ingrese el nombre del esquema:")

        if ok_pressed:
            folder_path = "../XML"
            new_file = os.path.join(folder_path, new_name + ".xml")
            shutil.copy(base_file, new_file)
            # Mostrar los archivos en el objeto list


            # Refrescar la lista de archivos después de duplicar el archivo
            self.refresh_file_list()

    def refresh_file_list(self):
        
        file_list = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        # Limpiar la lista actual y agregar los nuevos elementos
        self.list_schemes_model.clear()
        for file_name in file_list:
            item = QtGui.QStandardItem(file_name)
            self.list_schemes_model.appendRow(item)


    # Método que elimina los esquemas seleccionados
    def delete_scheme(self):
        selected_indexes = self.ui.list_schemes.selectedIndexes()

        dialog = QMessageBox()
        dialog.setWindowTitle("Confirmación")
        dialog.setText("¿Estás seguro de que deseas borrar el esquema?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = dialog.exec_()

        if response == QMessageBox.Yes:

            if selected_indexes:
                row = selected_indexes[0].row()
                item = self.list_schemes_model.item(row)

                file_to_delete = os.path.join(self.folder_path, item.text())

                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)

                    # Refrescar la lista de esquemas después de eliminar
                    self.refresh_file_list()
            else:
                print("No se ha seleccionado ningún elemento para eliminar.")
        
        else:
            print("No se ha eliminado el esquema")

    #Método para seleccionar los diseños que se quiere procesar      
    def select_designs(self):
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFiles)
            files_selected, _ = file_dialog.getOpenFileNames(self, "Seleccionar Archivos", "", "Archivos (*.tif *.psd *.psb)")

            if files_selected:
                # Extraer y guardar solo los nombres de los archivos
                self.file_names = [QFileInfo(self.file_path).fileName() for self.file_path in files_selected]
                self.selected_designs.extend(self.file_names)
                            
                # Mostrar los archivos en el objeto list
                for self.file_name2 in self.file_names:
                    self.item = QtGui.QStandardItem(self.file_name2)
                    self.list_designs_model.appendRow(self.item)


    # Método que elimina los diseños de la lista de diseños abiertos        
    def delete_designs(self):
        selected_indexes = self.ui.list_designs.selectedIndexes()
        #print("Variable selected indexes: "+selected_indexes)

        dialog = QMessageBox()
        dialog.setWindowTitle("Confirmación")
        dialog.setText("¿Estás seguro de que deseas borrar los diseños?")        
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = dialog.exec_()

        if response == QMessageBox.Yes:

            if selected_indexes:
                rows_to_remove = []
                for index in selected_indexes:
                    rows_to_remove.append(index.row())

                # Eliminar las filas correspondientes de la lista model
                for row in sorted(rows_to_remove, reverse=True):
                    self.list_designs_model.removeRow(row)
            else:
                print("No se ha seleccionado ningún diseño para eliminar.")
        else:
            print("No se borra ningún diseño")

    # Método para establecer la carpeta de salida
    def output_folder(self):
        self.output_folder_selected = QFileDialog.getExistingDirectoryUrl(self, "Seleccionar Carpeta", "")

        if self.output_folder_selected:
            self.output_folder_path = self.output_folder_selected.toLocalFile()
            self.defaultOutputPath = self.output_folder_path
            self.ui.caja_ruta.setText(self.defaultOutputPath)


    #Método para el procesado de archivos
    def process_files(self):
        selected_indexes = self.ui.list_schemes.selectedIndexes()
        if not selected_indexes:
            print("No se ha seleccionado ningún esquema.")
            return

        row = selected_indexes[0].row()
        item = self.list_schemes_model.item(row)
        print(f"Numero fila lista xml: {row}")

        scheme_file = os.path.join("../XML/", item.text())
        print(f"Ruta scheme_file: {scheme_file}")

        if not os.path.exists(scheme_file):
            print("El archivo del esquema no existe.")
            return
        
        self.output_folder_path = self.ui.caja_ruta.text()
        print("Ruta Output_folder_path: " +self.output_folder_path)

        if not self.output_folder_path:
            print("No se ha seleccionado una carpeta de salida.")
            return

        ####### Lectura de xml ########
        tree = ET.parse(scheme_file)
        
        self.listaCanalesSalida = []

        print("El orden de canales de salida del xml guardado en el array es:")

        for salida in tree.iter("salida"):
            for canal in salida.iter("canal"):
                orden = canal.get("numero")
                #print(f"Canal: ",orden)
                self.listaCanalesSalida.append(orden)

        print(self.listaCanalesSalida)

        self.numeroCanalesXML = len(self.listaCanalesSalida)
        print("El número de canales del xml es: ",self.numeroCanalesXML)
        
        # Crear un diálogo de progreso
        processDialog = QProgressDialog("Procesando archivos...", "Cancelar", 0, len(self.selected_designs), self)
        processDialog.setWindowTitle("Procesado")
        #processDialog.setLabelText("Working on file: ")
        processDialog.show()

        for i, self.design in enumerate(self.selected_designs):
            # Actualizar el progreso
            processDialog.setValue(i)
            processDialog.setLabelText(f"Working on file: {self.design}")
            

            self.file_path = os.path.join(os.path.dirname(self.file_path), self.design)

            if self.file_path.lower().endswith(('.psd', '.psb')):
                self.process_psd()
            elif self.file_path.lower().endswith('.tif'):
                self.process_tif()
            
            
            # Permitir que la GUI se actualice
            QApplication.processEvents()
        
        # Cerrar el diálogo al final del proceso
        processDialog.close()

        print(f"Ruta de los diseños: "+self.file_path)
        self.list_designs_model.clear()


    
        """
        # Método para crear los píxeles finales en vez de bucle anidado
        def generar_pixeles():
            for k in range(pixelesImagen):
                yield tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))


        # Convertir el generador a una tupla y pasarla a putdata
        psdPil.putdata(tuple(generar_pixeles()))
        print("putdata terminado")
        """


    ##### Método para procesado de psd/psb ######
    
    def process_psd(self):
        
        try:
            psd = psd_tools.PSDImage.open(self.file_path)

        except:
            print("No se ha podido abrir la imagen porque tiene más de 4 canales")

        numeroCanales = psd.channels
        print(f"Numero canales: {numeroCanales}")
        
        psdPil = psd.composite()
        
        if numeroCanales == self.numeroCanalesXML:
            
            listaCanalesOr = []

            datosCanal = psdPil.getdata()
            
            #print(f"Datos de los canales originales: {list(datosCanal)[:]} ")

            for i in range(numeroCanales):
                datosCanal = psdPil.getdata(i)
                #print(f"Datos de los canales originales: {list(datosCanal)[:]} ",i," canal")
                listaCanalesOr.append(list(datosCanal))
            
            #print(f"Print de listaCanalesOr: {list(listaCanalesOr)[:]}")

            pixelesImagen = psd.height*psd.width
            print(f"Los pixeles de la imagen son: {pixelesImagen}")
            
            ##### Construccion de los canales de salida ########        
            datosCanalesFinal = []
            listaPixelesFinal = []

            for i in range(numeroCanales):
                numeroCanalSalida = int(self.listaCanalesSalida[i])
                datosCanalSalida = psdPil.getdata(numeroCanalSalida)
                #print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
                datosCanalesFinal.append(datosCanalSalida)

            print("Proceso canales Salida terminado")
            #print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:]}")
            
            pixel = ()

            for k in range(pixelesImagen):
                pixel = tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))  # Crea una tupla por cada pixel
                listaPixelesFinal.append(pixel)  # Agrega la tupla a la lista
            print("bucle for canales final terminado")
            tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
            print("conversión tupla terminado")
            #print(f"Print de tuplaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

            psdPil.putdata(tuplaPixelesFinal) # Sobreescribe los pixeles del documento abierto en memoria
            
            print("Sobreescritura de pixeles finalizada")

            
                    
            design_output_path = os.path.join(self.output_folder_path, self.design)
            
            newPSD = psd.frompil(psdPil,compression=Compression.RAW)      
            print("conversión from Pil terminado")
            newPSD.save(design_output_path)
            print("Archivo guardado correctamente")
        
        else:
            print("El número de canales del XML y el diseño no coinciden")
    
    

    ######### Método TIF ###########

    def process_tif(self):
        try:
            tif = tifffile.imread(self.file_path)
        except Exception as e:
            print(f"No se ha podido abrir la imagen: {e}")
            return

        if tif.ndim < 3:
            print("La imagen no tiene suficientes dimensiones.")
            return

        numeroCanales = tif.shape[2]
        print(f"Número de canales: {numeroCanales}")

        if numeroCanales == self.numeroCanalesXML:
            print("numero Canales del diseño y XML coinciden")
        
            height, width, numeroCanales = tif.shape
            print(f"Dimensiones de la imagen: Alto={height}, Ancho={width}, Canales={numeroCanales}")

            # Lista para almacenar los valores de los píxeles
            lista_pixeles_Or = []

            # Bucle for anidado para recorrer cada píxel
            for y in range(height):
                for x in range(width):
                    # Obtener los valores de los canales para el píxel actual
                    pixel = tif[y, x, :]
                    # Convertir los valores a una lista y agregarlos a lista_pixeles
                    lista_pixeles_Or.append(pixel.tolist())

            print("Valores de los píxeles almacenados en lista_pixeles.")
            # Opcional: imprimir los primeros 10 píxeles para verificar
            print("Primeros 10 píxeles:", lista_pixeles_Or[:10])
                
            pixelesImagen = tif.shape[0]*tif.shape[1]
            print(f"Los pixeles de la imagen son: {pixelesImagen}")
            
            ##### Construccion de los canales de salida ########        
            datosCanalesFinal = []
            listaPixelesFinal = []

            for i in range(numeroCanales):
                numeroCanalSalida = int(self.listaCanalesSalida[i])
                datosCanalSalida = tif.getdata(numeroCanalSalida)
                #print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
                datosCanalesFinal.append(datosCanalSalida)

            print("Proceso canales Salida terminado")
            print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:10]}")


            """
            
            # Método para crear los píxeles finales en vez de bucle anidado
            def generar_pixeles():
                for k in range(pixelesImagen):
                    yield tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))


            # Convertir el generador a una tupla y pasarla a putdata
            psdPil.putdata(tuple(generar_pixeles()))
            print("putdata terminado")
            """
            """


            pixel = ()

            for k in range(pixelesImagen):
                pixel = tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))  # Crea una tupla por cada pixel
                listaPixelesFinal.append(pixel)  # Agrega la tupla a la lista
            print("bucle for canales final terminado")
            tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
            print("conversión tupla terminado")
            #print(f"Print de tuplaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

            

            design_output_path = os.path.join(self.output_folder_path, self.design)
            tifffile.imwrite(design_output_path, new_tif_data)

            print("Archivo guardado correctamente")
            """
        else:
            print("El número de canales del XML y el diseño no coinciden")
            return



    ##########################################################



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Aplicacion()
    myapp.show()
    myapp.crear_db_si_no_exite()
    sys.exit(app.exec())