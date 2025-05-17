import os


def inicializar_rutas_config():
    """
    Inicializa el archivo de configuración de rutas si no existe.
    Se llama al inicio de la aplicación para garantizar que el archivo existe.
    """
    try:
        # Obtener la ruta al directorio de configuración
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
        config_file = os.path.join(config_dir, "rutas_config.py")

        # Verificar si el archivo existe
        if not os.path.exists(config_file):
            print("Creando archivo de configuración de rutas...")

            # Contenido por defecto del archivo
            default_content = """# Configuración de rutas de archivos
                RUTAS_CONFIG = {
                    "ruta_salida": "",  # Se establecerá en tiempo de ejecución
                    "ip_servidor": "localhost"  # Valor por defecto
                }
                """

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