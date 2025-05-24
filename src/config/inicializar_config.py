import os
import textwrap

from src.config import rutas_config


def inicializar_rutas_config(es_admin):
    """
    Inicializa el archivo de configuración de rutas si no existe.
    Se llama al inicio de la aplicación para garantizar que el archivo existe.
    """
    try:
        # Obtener la ruta al directorio de configuración
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(config_dir, "rutas_config.py")

        # Verificar si el archivo existe
        if not os.path.exists(config_file):
            print("Creando archivo de configuración de rutas...")

            # Contenido por defecto del archivo
            default_content = textwrap.dedent(f"""
            # Configuracion de rutas de archivos
            RUTAS_CONFIG = {{
                "ruta_salida": "",  # Sin ruta por defecto
                "ip_servidor": "localhost"       # Valor por defecto
            }}
            """)

            # Aseguramos que el directorio config existe
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)

            # Crear el archivo
            with open(config_file, 'w') as f:
                f.write(default_content)

            print(f"Archivo de configuración creado: {config_file}")

        return True
    except Exception as e:
        print(f"Error al inicializar el archivo de configuración: {e}")
        return False