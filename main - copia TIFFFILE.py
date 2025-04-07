from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys,os
from os import listdir
from PySide6 import QtWidgets,QtGui
import shutil
import psd_tools
import xml.etree.ElementTree as ET


import psd_tools.compression
import psd_tools.psd
from ui import *
from psd_tools.psd import ImageData,image_data
from psd_tools.compression import compress, decompress
from psd_tools.constants import Compression
from psd_tools.psd.base import BaseElement
from psd_tools.utils import pack, read_fmt, write_bytes, write_fmt
from psd_tools.validators import in_
from PIL.Image import *
from PIL import Image
import ctypes
import tifffile as tiff
import numpy as np




class Aplicacion(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        alto = user32.GetSystemMetrics(1)
        print("El alto de la resolución de pantalla es: ",alto)
        
        super(Aplicacion, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()

        if alto <= 1600:
            self.ui.setupUi1080(self)

        else:
            self.ui.setupUi4k(self)

        # Obtener la lista de archivos xml en la carpeta
        self.folder_path = "XML"
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
            folder_path = "XML"
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
        print("Variable selected indexes: "+selected_indexes)
        if selected_indexes:
            rows_to_remove = []
            for index in selected_indexes:
                rows_to_remove.append(index.row())

            # Eliminar las filas correspondientes de la lista model
            for row in sorted(rows_to_remove, reverse=True):
                self.list_designs_model.removeRow(row)
        else:
            print("No se ha seleccionado ningún diseño para eliminar.")


    # Método para establecer la carpeta de salida
    def output_folder(self):
        self.output_folder_selected = QFileDialog.getExistingDirectoryUrl(self, "Seleccionar Carpeta", "")

        if self.output_folder_selected:
            self.folder_path = self.output_folder_selected.toLocalFile()
            self.ui.caja_ruta.setText(self.folder_path)


    #Método para el procesado de archivos
    def process_files(self):
        selected_indexes = self.ui.list_schemes.selectedIndexes()
        if not selected_indexes:
            print("No se ha seleccionado ningún esquema.")
            return

        row = selected_indexes[0].row()
        item = self.list_schemes_model.item(row)
        print(f"Numero fila lista xml: {row}")
        scheme_file = os.path.join("XML/", item.text())
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
        
        
        for self.design in self.selected_designs:
            self.file_path = os.path.join(os.path.dirname(self.file_path), self.design)
            if self.file_path.lower().endswith(('.psd', '.psb')):
                self.process_psd()
            elif self.file_path.lower().endswith('.tif'):
                self.process_tif()
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
        psd = psd_tools.PSDImage.open(self.file_path)

        numeroCanales = psd.channels
        print(f"Numero canales: {numeroCanales}")
        
        # Obtiene los datos de imagen (esto incluye todos los canales)
        image_data = psd.image_data

        # Descomprime y obtiene los datos de píxeles
        pixel_data = image_data.get_data(psd.header)

        # Si split es True, obtendrás una lista con los datos separados por canales
        if isinstance(pixel_data, list):
            for i, channel in enumerate(pixel_data):
                print(f"Datos del Canal {i}: {list(channel)[:10]}")  # Muestra solo los primeros 10 valores
        else:
            print("Los datos no están en formato esperado.")




        
        listaCanalesOr = []

        datosCanal = psdPil.getdata()
        
        print(f"Datos de los canales originales: {list(datosCanal)[:]} ")

        for i in range(numeroCanales):
            datosCanal = psdPil.getdata(i)
            print(f"Datos de los canales originales: {list(datosCanal)[:]} ",i," canal")
            listaCanalesOr.append(list(datosCanal))
        
        print(f"Print de listaCanalesOr: {list(listaCanalesOr)[:]}")

        pixelesImagen = psd.height*psd.width
        print(f"Los pixeles de la imagen son: {pixelesImagen}")
        
        ##### Construccion de los canales de salida ########        
        datosCanalesFinal = []
        listaPixelesFinal = []

        for i in range(numeroCanales):
            numeroCanalSalida = int(self.listaCanalesSalida[i])
            datosCanalSalida = psdPil.getdata(numeroCanalSalida)
            print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
            datosCanalesFinal.append(datosCanalSalida)

        print("Proceso canales Salida terminado")
        print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:]}")
        
        pixel = ()

        for k in range(pixelesImagen):
            pixel = tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))  # Crea una tupla por cada pixel
            listaPixelesFinal.append(pixel)  # Agrega la tupla a la lista
        print("bucle for canales final terminado")
        tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
        print("conversión tupla terminado")
        print(f"Print de tuplaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

        psdPil.putdata(tuplaPixelesFinal) # Sobreescribe los pixeles del documento abierto en memoria
        
        print("Sobreescritura de pixeles finalizada")

        
                
        design_output_path = os.path.join(self.output_folder_path, self.design)
        
        newPSD = psd.frompil(psdPil,compression=Compression.RAW)      
        print("conversión from Pil terminado")
        newPSD.save(design_output_path)
        print("Archivo guardado correctamente")
    
    
    """
    def process_psd(self):
        psd = psd_tools.PSDImage.open(self.file_path)

        numeroCanales = psd.channels
        print(f"Numero canales: {numeroCanales}")
        
        psdPil = psd.composite()
        
        listaCanalesOr = []

        datosCanal = psdPil.getdata()
        
        print(f"Datos de los canales originales: {list(datosCanal)[:]} ")

        for i in range(numeroCanales):
            datosCanal = psdPil.getdata(i)
            print(f"Datos de los canales originales: {list(datosCanal)[:]} ",i," canal")
            listaCanalesOr.append(list(datosCanal))
        
        print(f"Print de listaCanalesOr: {list(listaCanalesOr)[:]}")

        pixelesImagen = psd.height*psd.width
        print(f"Los pixeles de la imagen son: {pixelesImagen}")
        
        ##### Construccion de los canales de salida ########        
        datosCanalesFinal = []
        listaPixelesFinal = []

        for i in range(numeroCanales):
            numeroCanalSalida = int(self.listaCanalesSalida[i])
            datosCanalSalida = psdPil.getdata(numeroCanalSalida)
            print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
            datosCanalesFinal.append(datosCanalSalida)

        print("Proceso canales Salida terminado")
        print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:]}")
        
        pixel = ()

        for k in range(pixelesImagen):
            pixel = tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))  # Crea una tupla por cada pixel
            listaPixelesFinal.append(pixel)  # Agrega la tupla a la lista
        print("bucle for canales final terminado")
        tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
        print("conversión tupla terminado")
        print(f"Print de tuplaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

        psdPil.putdata(tuplaPixelesFinal) # Sobreescribe los pixeles del documento abierto en memoria
        
        print("Sobreescritura de pixeles finalizada")

        
                
        design_output_path = os.path.join(self.output_folder_path, self.design)
        
        newPSD = psd.frompil(psdPil,compression=Compression.RAW)      
        print("conversión from Pil terminado")
        newPSD.save(design_output_path)
        print("Archivo guardado correctamente")
        
    """
    

    ######### Método TIF ###########

    def process_tif(self):
        
        print("Versión Tifffile: ",tiff.__version__)
        # Abre el archivo TIFF
        tif = tiff.TiffFile(self.file_path)
        print(f"Número de páginas: {len(tif.pages)}")
        
        # Accede a la primera página (si hay varias)
        pagina = tif.pages[0]

        # Obtiene los datos de la imagen
        datos_imagen = tif.asarray()
        print(f"Print de datos_imagen: {(datos_imagen)[:]}")
        print(f"Forma de datos_imagen: {datos_imagen.shape}")
        # Verifica el número de canales
        numeroCanales = pagina.samplesperpixel
        print(f"Número de canales: {numeroCanales}")

        # Extrae cada canal
        lista_canales = [datos_imagen[:, :, i] for i in range(numeroCanales)]
        print(f"Print de lista_canales: {(lista_canales)[:]}")

        listaCanalesOr = []

        for i, canal in enumerate(lista_canales):
            print(f"Datos del canal {i}: {canal.flatten()[:]}")  # Muestra solo los primeros valores
            listaCanalesOr.append(canal.flatten().tolist())

        print(f"Print de listaCanalesOr: {(listaCanalesOr)[:]}")

        # Obtiene las dimensiones de la imagen
        altura, anchura = pagina.shape[:2]
        
        # Calcula el número de píxeles
        num_pixeles = altura * anchura

        print(f'El archivo TIFF tiene {num_pixeles} píxeles.')
        
        ##### Construccion de los canales de salida ########        
        datosCanalesFinal = []
        
        for i in range(numeroCanales):
            numeroCanalSalida = int(self.listaCanalesSalida[i])
            datosCanalSalida = listaCanalesOr[numeroCanalSalida]
            print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
            datosCanalesFinal.append(datosCanalSalida)

        print("Proceso canales Salida terminado")
        print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:]}")
       
        
        """
        # Método para crear los píxeles finales en vez de bucle anidado
        def generar_pixeles():
            for k in range(pixelesImagen):
                yield tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))


        # Convertir el generador a una tupla y pasarla a putdata
        psdPil.putdata(tuple(generar_pixeles()))
        print("putdata terminado")
        """
        listaPixelesFinal = []
        pixel = []

        for k in range(num_pixeles):
            pixel = [datosCanalesFinal[j][k] for j in range(numeroCanales)]  # Crea un array por cada pixel
            listaPixelesFinal.append(pixel)  # Agrega el array a la lista/array
        print("bucle for canales final terminado")
        print(f"Print de listaPixelesFinal: {list(listaPixelesFinal)[:]}")
        #tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
        #print("conversión tupla terminado")
        #print(f"Print de listaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

        # Crear un array vacío para los píxeles finales
        datos_final = np.zeros((altura, anchura, numeroCanales), dtype=int)

        datos_final = listaPixelesFinal
        
        """
        # Llenar el array con los datos de cada canal
        for i in range(anchura):
            for j in range(altura):
                for k in range(numeroCanales):
                    datos_final[i][j][k] = datosCanalesFinal[k][(i * anchura) + j]
                    #print(f"Print de datos_finales: {(datos_final)[:]}")
        print(f"Print de datos_finales: {(datos_final)[:]}")
        """
        design_output_path = os.path.join(self.output_folder_path, self.design)
        # Guardar como TIFF interleaved
        with tiff.TiffWriter(design_output_path) as tif:
            tif.write(datos_final, photometric='cmyk', extrasamples=[1, 1])

        

        #tiff.imwrite(design_output_path, datos_final)

        print("Archivo guardado correctamente")

        tif.close()
        


    ##########################################################



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Aplicacion()
    myapp.show()
    sys.exit(app.exec_())