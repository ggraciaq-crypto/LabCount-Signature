
# LabCount

## Sistema de Conteo de Personas para Laboratorio

LabCount es una aplicación web desarrollada para detectar y contar personas presentes en un laboratorio mediante una cámara en tiempo real.

El sistema utiliza visión por computadora para identificar personas, calcular el porcentaje de ocupación y mostrar el estado del aforo del laboratorio.

Además, permite almacenar los registros de conteo en una base de datos PostgreSQL.

## Objetivo

Desarrollar un sistema web que permita detectar y contabilizar personas mediante una cámara, utilizando técnicas de visión por computadora para facilitar el monitoreo de la ocupación de un laboratorio.

## Tecnologías utilizadas

- Python
- Django
- OpenCV
- YOLOv8
- PostgreSQL
- HTML
- CSS
- JavaScript

## Funcionalidades

- Visualización de la cámara en tiempo real.
- Detección automática de personas.
- Identificación visual mediante recuadros.
- Conteo de personas presentes.
- Inicio, detención y reinicio de la cámara.
- Visualización de la capacidad máxima del laboratorio.
- Cálculo automático del porcentaje de ocupación.
- Identificación del estado del aforo.
- Almacenamiento de registros en PostgreSQL.
- Interfaz web adaptable a diferentes tamaños de pantalla.

## Funcionamiento

La aplicación utiliza OpenCV para capturar imágenes de la cámara.

Posteriormente, YOLOv8 analiza las imágenes para detectar personas y dibujar recuadros alrededor de ellas.

Django procesa la información y permite visualizar los resultados mediante una interfaz web.

El sistema considera una capacidad máxima de 10 personas.

El porcentaje de ocupación se calcula mediante:

Porcentaje de ocupación = (Personas detectadas / Capacidad máxima) × 100

Cuando la cantidad de personas detectadas alcanza o supera la capacidad máxima, el sistema muestra el estado "Aforo completo".

En caso contrario, muestra el estado "Seguro".

Los registros se almacenan automáticamente en PostgreSQL.

## Requisitos

- Python 3.11
- PostgreSQL
- Cámara web
- Conexión a Internet para instalar las dependencias

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd LabCount
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar PostgreSQL

Crear una base de datos llamada:

```text
labcount_db
```

Configurar la conexión a PostgreSQL de acuerdo con los valores establecidos en `labcount_config/settings.py`.

La contraseña se proporciona mediante la variable de entorno `LABCOUNT_DB_PASSWORD`.

En PowerShell:

```powershell
$env:LABCOUNT_DB_PASSWORD = Read-Host "Contraseña de PostgreSQL"
```

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

### 8. Abrir la aplicación

Ingresar en el navegador:

http://127.0.0.1:8000/

## Uso del sistema

1. Abrir LabCount en el navegador.
2. Presionar el botón "Iniciar Cámara".
3. Permitir que el sistema detecte las personas presentes.
4. Observar el conteo y el porcentaje de ocupación.
5. Consultar el estado del aforo.
6. Utilizar "Detener" para finalizar la transmisión.
7. Utilizar "Reiniciar" para volver a iniciar la cámara.

## Base de datos

El sistema utiliza PostgreSQL para almacenar los registros de conteo.

La tabla `registro_conteo` contiene:

- Identificador del registro.
- Fecha y hora.
- Personas detectadas.
- Capacidad máxima.
- Porcentaje de ocupación.
- Estado del aforo.

Los registros se guardan periódicamente y cuando cambia el conteo, respetando un intervalo mínimo entre determinados registros.

## Pruebas

El proyecto incluye pruebas automáticas desarrolladas con Django.

Para ejecutarlas:

```bash
python manage.py test detector
```

Las pruebas permiten verificar la carga de la página principal, la respuesta del contador y las operaciones básicas del modelo de registros.

## Limitaciones

La precisión del conteo depende de la iluminación, la posición de las personas y la visibilidad de la cámara.

El sistema contabiliza las detecciones visibles en cada imagen, por lo que no realiza un seguimiento de entradas y salidas individuales.

La aplicación está diseñada para ejecutarse localmente como prototipo académico.

## Estado del proyecto

Prototipo funcional desarrollado con Django, OpenCV, YOLOv8 y PostgreSQL.
