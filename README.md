# Swiper

**Swiper** es una aplicación de escritorio desarrollada en Python y PySide6 para gestionar esquemas de canales (por ejemplo, CMYK) y su flujo de procesamiento. Incluye componentes personalizados, conectividad a PostgreSQL y una interfaz moderna.

---

## Estructura del proyecto

```
Swiper/
├── main.py                 # Punto de entrada de la aplicación
├── src/
│   ├── controllers/
│   │   └── crear_db.py     # Inicialización de la base de datos y creación de tablas
│   ├── img/
│   │   └── Logo.png        # Logotipo de la aplicación
│   ├── ui/
│   │   └── ui.py           # `SwiperUI`: construcción de la vista (widgets, layouts)
│   ├── views/
│   │   └── MainWindow.py   # `QMainWindow` que monta `SwiperUI` y configura la ventana
│   └── widgets/
│       └── boton_canal.py  # `Boton_canal`: QPushButton tipo “pastilla” para canales
└── README.md               # Documentación del proyecto
```

---

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/Swiper.git
   cd Swiper
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\\Scripts\\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install PySide6 psycopg[binary]
   ```

---

## Inicializar base de datos

Antes de ejecutar la app, es necesario crear la base de datos y las tablas definidas en `src/controllers/crear_db.py`:

```bash
python - <<EOF
from src.controllers.crear_db import Crear_db
Crear_db.crear_db_si_no_exite()
EOF
```

Esto:

- Crea la base de datos `swiper` (si no existe).
- Define las tablas: `usuarios`, `esquemas`, `centros_productivos`, `accesos`.
- Inserta un usuario admin por defecto.

---

## Uso

Para arrancar la aplicación:

```bash
python main.py
```

Aparecerá la ventana principal con:

- **Barra superior**: logo + título `SWIPER` con efecto de tarjeta y sombra.
- **Menú de esquemas**: botones *Añadir*, *Editar*, *Eliminar* y *Configuración*.
- **Área de trabajo**: cuatro columnas (`Esquemas`, `Entrada`, `Salida`, `Procesado`), cada una con un contenedor donde se agregarán los canales.
- **Botones personalizados**: los canales se representan con `Boton_canal`, un botón checkable estilo “pill” con selección exclusiva.

---

## Componentes principales

- **`main.py`**\
  Punto de entrada que inicia `QApplication` y muestra `MainWindow`.

- **`src/views/MainWindow.py`**\
  `MainWindow(QMainWindow)` monta `SwiperUI` y configura icono, título y tamaño.

- **`src/ui/ui.py`**\
  Clase `SwiperUI(QWidget)` que construye toda la interfaz (layouts, frames, botones y señalización básica).

- **`src/widgets/boton_canal.py`**\
  `Boton_canal(QPushButton)` un botón personalizado para representar canales; cambia de estilo al seleccionarse y pertenece a un `QButtonGroup` exclusivo.

- **`src/controllers/crear_db.py`**\
  Lógica para crear la base de datos y las tablas necesarias, con valores por defecto (timestamp, usuario admin).

---

## Próximos pasos y mejoras

- **Separar lógica y controladores**: crear un paquete `controllers/` con clases que respondan a eventos y manejen operaciones de negocio.
- **Servicios y modelos**: añadir carpetas `services/` (acceso a datos) y `models/` (`@dataclass` para entidades).
- **Drag & Drop**: implementar la funcionalidad para arrastrar y soltar botones de canal entre columnas.
- **Pruebas unitarias**: incorporar `pytest` para testear controladores y servicios sin UI.
- **Configuración**: usar `.env` o `config.py` para variables de entorno y credenciales.
- **Empaquetado**: generar instaladores multiplataforma (PyInstaller, briefcase).

---
