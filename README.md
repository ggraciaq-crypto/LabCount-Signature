# LabCount Signature
## Sistema inteligente de detección y conteo de personas para laboratorios

### Descripción del proyecto

**LabCount Signature** es una aplicación web desarrollada para detectar y contabilizar personas presentes en un laboratorio mediante una cámara web y técnicas de visión por computadora.

El sistema utiliza el modelo de inteligencia artificial **YOLOv8**, junto con OpenCV, para identificar personas en las imágenes capturadas. Las detecciones se representan visualmente mediante recuadros, lo que permite reconocer a las personas identificadas por el sistema.

Además, la aplicación muestra el número de personas detectadas, la capacidad máxima establecida para el laboratorio, el porcentaje de ocupación y el estado del aforo.

El proyecto fue desarrollado con Django y utiliza PostgreSQL para almacenar los registros de conteo.

Se trata de un prototipo académico diseñado para funcionar localmente desde una computadora con cámara web.

---

## 1. Objetivo general

Desarrollar una aplicación web que permita detectar y contabilizar personas mediante una cámara, utilizando inteligencia artificial y técnicas de visión por computadora para facilitar el monitoreo de la ocupación de un laboratorio.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3.11 | Lenguaje de programación principal del sistema. |
| Django | Framework utilizado para desarrollar la aplicación web y gestionar las solicitudes. |
| YOLOv8 | Modelo de inteligencia artificial encargado de detectar personas. |
| OpenCV | Biblioteca utilizada para procesar imágenes y representar las detecciones. |
| PostgreSQL | Sistema gestor de base de datos utilizado para almacenar los registros de conteo. |
| HTML | Estructura de la interfaz web. |
| CSS | Diseño visual y adaptación de la interfaz. |
| JavaScript | Control de la cámara y actualización de la información en el navegador. |

## 3. Funcionalidades principales

El sistema dispone de las siguientes funcionalidades:

- Visualización de la cámara web.
- Detección automática de personas mediante YOLOv8.
- Identificación visual de las personas mediante recuadros.
- Visualización de la etiqueta «Persona» en las detecciones.
- Conteo de personas detectadas.
- Botón para iniciar la cámara.
- Botón para detener la cámara.
- Botón para reiniciar la cámara.
- Visualización de la capacidad máxima del laboratorio.
- Cálculo automático del porcentaje de ocupación.
- Identificación del estado del aforo.
- Almacenamiento de registros de conteo en PostgreSQL.
- Interfaz web adaptable a diferentes tamaños de pantalla.

## 4. Funcionamiento del sistema

El funcionamiento de LabCount Signature se desarrolla mediante las siguientes etapas:

**1. Activación de la cámara**

El usuario accede a la aplicación desde el navegador y presiona el botón «Iniciar cámara». El navegador solicita permiso para utilizar la cámara web.

**2. Captura de imágenes**

Una vez activada, la cámara permite visualizar el entorno del laboratorio. El sistema obtiene imágenes para realizar el análisis correspondiente.

**3. Detección de personas**

Las imágenes son procesadas mediante Django, OpenCV y el modelo YOLOv8n, configurado para identificar personas.

**4. Identificación visual**

Las personas detectadas se representan mediante recuadros y la etiqueta «Persona», facilitando su identificación en la imagen.

**5. Conteo de personas**

El sistema determina la cantidad de personas detectadas y actualiza la información presentada en la interfaz.

**6. Cálculo de ocupación**

A partir del conteo obtenido, se calcula el porcentaje de ocupación del laboratorio.

**7. Registro de información**

Los resultados del conteo se almacenan en una base de datos PostgreSQL para conservar la información registrada durante el funcionamiento del sistema.

## 5. Control del aforo

Para el desarrollo del prototipo se estableció una capacidad máxima de **10 personas**.

El porcentaje de ocupación se calcula mediante la siguiente fórmula:

**Porcentaje de ocupación = (Personas detectadas / Capacidad máxima) × 100**

### Ejemplo de funcionamiento

Si se detectan 4 personas:

Porcentaje de ocupación = (4 / 10) × 100

**Resultado: 40 % de ocupación.**

### Estados del aforo

| Condición | Estado mostrado |
|---|---|
| Menos de 10 personas detectadas | Seguro |
| 10 o más personas detectadas | Aforo completo |

Estos estados permiten identificar si la cantidad de personas detectadas se encuentra por debajo de la capacidad establecida o si la ha alcanzado.

## 6. Requisitos para ejecutar el proyecto

Para ejecutar LabCount Signature localmente se requiere:

- Python 3.11.
- PostgreSQL instalado y configurado.
- Una computadora con cámara web.
- Un navegador web actualizado.
- Conexión a Internet para descargar las dependencias necesarias.
- Acceso al código fuente del proyecto.

## 7. Instalación y configuración

### Paso 1. Clonar el repositorio

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/ggraciaq-crypto/LabCount-Signature.git
```

Ingresar a la carpeta descargada:

```bash
cd LabCount-Signature
```

### Paso 2. Crear un entorno virtual

```bash
python -m venv venv
```

### Paso 3. Activar el entorno virtual

En Windows, utilizando PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Paso 4. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

Este comando instalará las dependencias declaradas en el proyecto.

### Paso 5. Configurar PostgreSQL

Crear una base de datos con el nombre:

```text
labcount_db
```

Configurar la conexión de acuerdo con los parámetros definidos en:

```text
labcount_config/settings.py
```

La contraseña de PostgreSQL se proporciona mediante la variable de entorno `LABCOUNT_DB_PASSWORD`.

En PowerShell:

```powershell
$env:LABCOUNT_DB_PASSWORD = Read-Host "Contraseña de PostgreSQL"
```

La configuración de la base de datos debe coincidir con los valores establecidos en el archivo de configuración de Django.

### Paso 6. Aplicar las migraciones

```bash
python manage.py migrate
```

Este comando permite crear las tablas necesarias en la base de datos, de acuerdo con las migraciones del proyecto.

### Paso 7. Iniciar el servidor local

```bash
python manage.py runserver
```

### Paso 8. Abrir la aplicación

Ingresar desde el navegador a la siguiente dirección:

http://127.0.0.1:8000/

Una vez cargada la página principal, se podrá utilizar la interfaz de LabCount Signature.

## 8. Uso del sistema

Para utilizar la aplicación se deben seguir los siguientes pasos:

1. Abrir LabCount Signature en el navegador.
2. Presionar el botón «Iniciar cámara».
3. Autorizar el acceso a la cámara web, si el navegador lo solicita.
4. Ubicarse dentro del campo de visión de la cámara.
5. Observar las detecciones realizadas mediante los recuadros de identificación.
6. Consultar el número de personas detectadas.
7. Verificar la capacidad máxima y el porcentaje de ocupación.
8. Observar el estado del aforo.
9. Presionar «Detener» para finalizar el uso de la cámara.
10. Utilizar «Reiniciar» para comenzar nuevamente el proceso.

## 9. Base de datos

LabCount Signature utiliza **PostgreSQL** para almacenar los registros generados durante el conteo de personas.

El modelo `RegistroConteo` contempla los siguientes datos:

| Campo | Descripción |
|---|---|
| Identificador | Identifica cada registro almacenado. |
| Fecha y hora | Indica cuándo se generó el registro. |
| Personas detectadas | Cantidad de personas identificadas. |
| Capacidad máxima | Límite de personas establecido para el laboratorio. |
| Porcentaje de ocupación | Porcentaje calculado a partir del conteo. |
| Estado del aforo | Estado correspondiente a la ocupación detectada. |

El almacenamiento permite conservar información de las detecciones realizadas durante el funcionamiento del sistema.

## 10. Pruebas del proyecto

El proyecto incluye un módulo de pruebas de Django.

Para ejecutar las pruebas automáticas se utiliza:

```bash
python manage.py test detector
```

Las pruebas permiten comprobar las funcionalidades contempladas en los casos de prueba implementados.

Adicionalmente, el sistema puede verificarse manualmente mediante:

- Activación y detención de la cámara.
- Detección de una o varias personas.
- Visualización de los recuadros de identificación.
- Actualización del conteo.
- Cálculo del porcentaje de ocupación.
- Visualización del estado del aforo.
- Comprobación de los registros almacenados en PostgreSQL.

## 11. Limitaciones del sistema

Al tratarse de un prototipo académico, se consideran las siguientes limitaciones:

- La precisión de las detecciones puede variar según la iluminación del entorno.
- Las personas parcialmente ocultas pueden no ser identificadas correctamente.
- La distancia y el ángulo de la cámara pueden influir en los resultados.
- El rendimiento depende de las características de la computadora utilizada.
- El sistema contabiliza las personas visibles en las imágenes analizadas y no realiza un seguimiento individual de entradas y salidas.
- La aplicación está orientada a su ejecución local y no requiere un despliegue público para su demostración académica.

## 12. Estado del proyecto

**Estado: Prototipo académico funcional en entorno local.**

LabCount Signature integra una interfaz web con detección de personas mediante inteligencia artificial, conteo de ocupación y almacenamiento de registros en PostgreSQL.

El proyecto permite demostrar la aplicación de Django, Python, OpenCV y YOLOv8 en una solución de monitoreo de aforo para laboratorios.

---

**Proyecto académico: LabCount Signature**

**Repositorio:** https://github.com/ggraciaq-crypto/LabCount-Signature
