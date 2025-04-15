# Método para el procesado de archivos
import os
from PySide6.QtWidgets import QProgressDialog
from PySide6 import QApplication
import psd_tools
import xml.etree.ElementTree as ET
import psd_tools.compression
import psd_tools.psd
from psd_tools.constants import Compression
import tifffile



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
    print("Ruta Output_folder_path: " + self.output_folder_path)

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
            # print(f"Canal: ",orden)
            self.listaCanalesSalida.append(orden)

    print(self.listaCanalesSalida)

    self.numeroCanalesXML = len(self.listaCanalesSalida)
    print("El número de canales del xml es: ", self.numeroCanalesXML)

    # Crear un diálogo de progreso
    processDialog = QProgressDialog("Procesando archivos...", "Cancelar", 0, len(self.selected_designs), self)
    processDialog.setWindowTitle("Procesado")
    # processDialog.setLabelText("Working on file: ")
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

    print(f"Ruta de los diseños: " + self.file_path)
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

        # print(f"Datos de los canales originales: {list(datosCanal)[:]} ")

        for i in range(numeroCanales):
            datosCanal = psdPil.getdata(i)
            # print(f"Datos de los canales originales: {list(datosCanal)[:]} ",i," canal")
            listaCanalesOr.append(list(datosCanal))

        # print(f"Print de listaCanalesOr: {list(listaCanalesOr)[:]}")

        pixelesImagen = psd.height * psd.width
        print(f"Los pixeles de la imagen son: {pixelesImagen}")

        ##### Construccion de los canales de salida ########
        datosCanalesFinal = []
        listaPixelesFinal = []

        for i in range(numeroCanales):
            numeroCanalSalida = int(self.listaCanalesSalida[i])
            datosCanalSalida = psdPil.getdata(numeroCanalSalida)
            # print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
            datosCanalesFinal.append(datosCanalSalida)

        print("Proceso canales Salida terminado")
        # print(f"Print de datosCanalesFinal: {list(datosCanalesFinal)[:]}")

        pixel = ()

        for k in range(pixelesImagen):
            pixel = tuple(datosCanalesFinal[j][k] for j in range(numeroCanales))  # Crea una tupla por cada pixel
            listaPixelesFinal.append(pixel)  # Agrega la tupla a la lista
        print("bucle for canales final terminado")
        tuplaPixelesFinal = tuple(listaPixelesFinal)  # Convierte la lista en tupla
        print("conversión tupla terminado")
        # print(f"Print de tuplaPixelesFinal: {list(tuplaPixelesFinal)[:]}")

        psdPil.putdata(tuplaPixelesFinal)  # Sobreescribe los pixeles del documento abierto en memoria

        print("Sobreescritura de pixeles finalizada")

        design_output_path = os.path.join(self.output_folder_path, self.design)

        newPSD = psd.frompil(psdPil, compression=Compression.RAW)
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

        pixelesImagen = tif.shape[0] * tif.shape[1]
        print(f"Los pixeles de la imagen son: {pixelesImagen}")

        ##### Construccion de los canales de salida ########
        datosCanalesFinal = []
        listaPixelesFinal = []

        for i in range(numeroCanales):
            numeroCanalSalida = int(self.listaCanalesSalida[i])
            datosCanalSalida = tif.getdata(numeroCanalSalida)
            # print(f"Print de datosCanalSalida: {list(datosCanalSalida)[:]} ", i, " canal")
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