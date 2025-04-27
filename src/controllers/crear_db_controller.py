from ..db.crear_db import CrearDB

class CrearDBController:

    # Controlador para inicializar la base de datos al arrancar la aplicación.


    def inicializar(self):
        try:
            CrearDB.crear_db_si_no_existe()
            print("Inicialización de base de datos completada.")
        except Exception as e:
            print("Error en inicialización:", e)
            raise
