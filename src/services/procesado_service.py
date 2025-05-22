import os

import psd_tools
from PIL.Image import *
from PIL import Image
from psd_tools.constants import Compression
from src.controllers.main_window_controller import MainWindowController


class ProcesadoService:
    def __init__(self,view):
        self.view = view

    def procesado(self,diseno,ruta_salida):
        # Controladores y listas de canales
        main_window_controller = MainWindowController(self.view)
        lista_canales_entrada = main_window_controller.obtener_nombre_orden_botones_entrada()
        lista_canales_salida = main_window_controller.obtener_nombre_orden_botones_salida()

        # Flag para rastrear si el procesado ha sido exitoso
        procesado_exitoso = True

        try:
            ruta_archivo = diseno.lower()
            print("ruta_archivo: ",ruta_archivo)
            if ruta_archivo.endswith(('.psd', '.psb')):
                ok = self.procesar_psd(
                    ruta_archivo,
                    lista_canales_entrada,
                    lista_canales_salida,
                    ruta_salida)
            elif ruta_archivo.endswith('.tif'):
                ok = self.procesar_tif(
                    ruta_archivo,
                    lista_canales_entrada,
                    lista_canales_salida,
                    ruta_salida)
            else:
                ok = False
            if not ok:
                procesado_exitoso = False
        except Exception as e:
            print(f"Error procesando {diseno}: {e}")
            procesado_exitoso = False
        return procesado_exitoso

    @staticmethod
    def procesar_psd(ruta_archivo,lista_canales_entrada,lista_canales_salida,ruta_salida):
        try:
            # Normalizar la ruta para prevenir problemas con barras
            ruta_archivo_normalizada = os.path.normpath(ruta_archivo)
            print("ruta_archivo_normalizada",ruta_archivo_normalizada)

            # Abrimos el archivo
            psd = psd_tools.PSDImage.open(ruta_archivo_normalizada)
            print("archivo abierto")

            # Obtener el modo de color para manejar CMYK correctamente
            modo_color = psd.color_mode.name
            print(f"Modo de color: {modo_color}")
            es_cmyk = modo_color == 'CMYK'

            numero_canales = psd.channels
            print("Numero de canales del diseño: ", numero_canales)

            numero_canales_esquema = len(lista_canales_entrada)
            print("Numero de canales del esquema: ",numero_canales_esquema)

            # Obtenemos imagen compuesta (solo el fondo sin las capas)
            psdPil = psd.composite()

            if numero_canales != numero_canales_esquema:
                print(f"El número de canales del esquema ({numero_canales_esquema}) "
                      f"y el diseño ({numero_canales}) no coinciden")
                return False

            # 1. Obtener los datos originales de todos los canales
            datos_canales_originales = []
            for i in range(numero_canales):
                datos_canal = list(psdPil.getdata(i))
                # Si es CMYK, invertir los valores (255 - valor)
                if es_cmyk:
                    datos_canal = [255 - valor for valor in datos_canal]

                datos_canales_originales.append(datos_canal)

            # 2. Construir el mapping: color → posición en lista_canales_entrada
            mapping_entrada = {color: idx for idx, color in enumerate(lista_canales_entrada)}
            """El mapping asocia el nombre del color con el canal de entrada, 
            de modo que luego se busca el color en el punto 2 en el mapping 
            según el orden de los canales de salida para añadirlos a la lista en ese orden"""

            # 3. Preparar la lista de datos de canales en el nuevo orden
            lista_datos_canales_final = []
            for color_salida in lista_canales_salida:
                # Buscar qué posición tiene este color en la lista de entrada
                idx_canal_entrada = mapping_entrada[color_salida]
                # Añadir los datos de ese canal a la lista final
                lista_datos_canales_final.append(datos_canales_originales[idx_canal_entrada])

            # 4. Reconstrucción de píxeles con generator
            """De este modo se llama al generador por cada píxel y así no se carga toda la lista de píxeles en memoria"""
            total_pixeles_imagen = psd.width * psd.height
            print(f"Los pixeles de la imagen son: {total_pixeles_imagen}")

            # Generador de pixeles permutados
            def pixel_stream():
                for i in range(total_pixeles_imagen):
                    pixel = tuple(lista_datos_canales_final[c][i] for c in range(len(lista_datos_canales_final)))
                    yield pixel

            # 5. Aplicar los nuevos datos a la imagen
            psdPil.putdata(list(pixel_stream()))
            print("Sobreescritura de pixeles finalizada")

            # 6. Guardado
            nombre_archivo = os.path.basename(ruta_archivo)
            nombre_ruta_final = os.path.join(ruta_salida,nombre_archivo)
            new_psd = psd.frompil(psdPil, compression=Compression.RAW)
            new_psd.save(nombre_ruta_final)
            return True

        except Exception as e:
            print(f"Error al procesar archivo PSD: {e}")
            return False

    @staticmethod
    def procesar_tif(ruta_archivo,lista_canales_entrada,lista_canales_salida,ruta_salida):
        tif = None
        try:
            # Normalizar la ruta para prevenir problemas con barras
            ruta_archivo_normalizada = os.path.normpath(ruta_archivo)
            print("ruta_archivo_normalizada",ruta_archivo_normalizada)

            # Abrimos el archivo
            try:
                tif = Image.open(ruta_archivo_normalizada)
            except Exception as e:
                print(f"No se ha podido abrir la imagen porque tiene más de 4 canales: {e}")
            print("archivo abierto")

            numero_canales = len(tif.getbands())
            print("Numero de canales del diseño: ", numero_canales)

            numero_canales_esquema = len(lista_canales_entrada)
            print("Numero de canales del esquema: ",numero_canales_esquema)

            if numero_canales != numero_canales_esquema:
                print(f"El número de canales del esquema ({numero_canales_esquema}) "
                      f"y el diseño ({numero_canales}) no coinciden")
                return False

            # 1. Obtener los datos originales de todos los canales
            datos_canales_originales = []
            for i in range(numero_canales):
                datos_canales_originales.append(tif.getdata(i))

            # 2. Construir el mapping: color → posición en lista_canales_entrada
            mapping_entrada = {color: idx for idx, color in enumerate(lista_canales_entrada)}
            """El mapping asocia el nombre del color con el canal de entrada, 
            de modo que luego se busca el color en el punto 2 en el mapping 
            según el orden de los canales de salida para añadirlos a la lista en ese orden"""

            # 3. Preparar la lista de datos de canales en el nuevo orden
            lista_datos_canales_final = []
            for color_salida in lista_canales_salida:
                # Buscar qué posición tiene este color en la lista de entrada
                idx_canal_entrada = mapping_entrada[color_salida]
                # Añadir los datos de ese canal a la lista final
                lista_datos_canales_final.append(datos_canales_originales[idx_canal_entrada])

            # 4. Reconstrucción de píxeles con generator
            """De este modo se llama al generador por cada píxel y así no se carga toda la lista de píxeles en memoria"""
            total_pixeles_imagen = tif.width * tif.height
            print(f"Los pixeles de la imagen son: {total_pixeles_imagen}")

            # Generador de pixeles permutados
            def pixel_stream():
                for i in range(total_pixeles_imagen):
                    yield tuple(lista_datos_canales_final[c][i] for c in range(len(lista_datos_canales_final)))

            # 5. Aplicar los nuevos datos a la imagen
            tif.putdata(list(pixel_stream()))
            print("Sobreescritura de pixeles finalizada")

            # 6. Guardado
            nombre_archivo = os.path.basename(ruta_archivo)
            nombre_ruta_final = os.path.join(ruta_salida,nombre_archivo)
            print("Ruta de guardado: ", nombre_ruta_final)
            tif.save(nombre_ruta_final)

            return True

        except Exception as e:
            print(f"Error al procesar archivo PSD: {e}")
            return False

