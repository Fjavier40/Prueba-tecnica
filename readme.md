# Prueba Técnica: Procesamiento de Datos y Creación de API
Este repositorio contiene la solución de la prueba técnica, que incluye:

1. Procesamiento y transferencia de datos (carga, extracción, transformación y dispersión en base de datos).
2. Creación de una API que calcula el número faltante de un conjunto de los primeros 100 números.
## Requisitos
- Python 3.11.4  
- PostgreSQL 
- pip (para instalar dependencias)
- FastAPI
- Uvicorn (para correr la API)
## Instalación
1. Clonar el repositorio:
git clone <URL_DEL_REPOSITORIO>
cd <CARPETA_DEL_PROYECTO>
## Crear y activar entorno virtual
python -m venv mi_entorno
- Windows
mi_entorno\Scripts\activate
- Linux / MacOS
source mi_entorno/bin/actívate
## Instalar dependencias
- pip install -r requirements.txt
## Configurar la base de datos PostgreSQL y crear la base de datos necesaria.
- 1. Instalar PostgreSQL
Windows / macOS / Linux:
Descarga desde https://www.postgresql.org/download/
 y sigue el asistente de instalación.

Durante la instalación, guarda o recuerdda la contraseña que definiste 
Puerto (por defecto: 5432)

## Ajustar los parámetros de conexión en el archivo ejemplo.env y renombralo como .env:
- ejemplo:
    - DB_NAME_DEFAULT=postgres       # Base de datos predeterminada (generalmente llamada 'postgres')
    - DB_NAME=etl_db                 # Base de datos que se creará por el script, (no lo cambies, debe ser "etl_db")
    - DB_USER=postgres               # Usuario de PostgreSQL
    - DB_PASSWORD=tu_contraseña      # Contraseña definida al instalar PostgreSQL
    - DB_HOST=localhost              # Host de conexión
    - DB_PORT=5432                   # Puerto de conexión (por defecto 5432)

## Ejecucion de la Seccion 1
Cambiar la carpeta Seccion 1 y ejecuctar en la terminal:
- 1.1.
    - python cargar_informacion.py      # carga el dataset crudo en la base de datos etl_db en la tabla raw_data
- 1.2.
    - python extraccion.py    # Carga los datos de la tabla anterior y lo guarda en formato csv con el nombre raw_data_extracted.csv para seguir con la  transformación
- 1.3.
    - python transformacion.py # Carga el archivo raw_data_extracted.csv y realiza las transformaciones para cumplir con el esquema, guarda el archivo listo en formato csv con el nombre transformed_data.csv' y lo carga a la base de datos en la tabla transformed data
- 1.4.
    - python dispersion_informacion.py  # crea las tablas 'charges' y 'companies' y carga los datos a dichas tablas. (Se añade imagen del diagrama)
- 1.5. 
    - python vista_sql.py  #Se crea la vista  en la base de datos con el nombre de: daily_company_totals

## Ejecucion de la Seccion 2
Cambiar a la carpeta Seccion 2 y ejecutar en la terminal
- uvicorn api:app --reload

Abrir el navegador y acceder a la API en http://127.0.0.1:8000
Extraer un número usando path en la barra de direcciones
ejemplo:
http://127.0.0.1:8000/extract/42


## NOTAS

- Se agregan los archivos analisis_extraccion.ipynb y Analisis_transformacion.ipynb donde se hizo el analisis de los datos para crear el script que los transforma. Así también se agrega el archivo de imagen: Diagrama base de datos.