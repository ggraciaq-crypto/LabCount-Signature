
import cv2
import numpy as np
import threading
import time

from django.db import close_old_connections
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .camara import DetectorPersonas
from .models import RegistroConteo


# Detector compartido para evitar cargar YOLOv8
# nuevamente en cada imagen.
detector = None
bloqueo_detector = threading.Lock()

# Control del registro en la base de datos.
bloqueo_registro = threading.Lock()
ultimo_conteo_guardado = None
ultimo_registro = 0

CAPACIDAD_MAXIMA = 10

@ensure_csrf_cookie
def inicio(request):
    return render(request, "detector/inicio.html")


def obtener_detector():
    global detector

    if detector is None:
        detector = DetectorPersonas()

    return detector


def calcular_estadisticas(cantidad):
    ocupacion = round(
        (cantidad / CAPACIDAD_MAXIMA) * 100
    )

    if cantidad >= CAPACIDAD_MAXIMA:
        estado = "Aforo completo"
    else:
        estado = "Seguro"

    return {
        "personas": cantidad,
        "capacidad": CAPACIDAD_MAXIMA,
        "ocupacion": ocupacion,
        "estado": estado
    }


def guardar_registro(cantidad, datos):
    global ultimo_conteo_guardado
    global ultimo_registro

    with bloqueo_registro:
        tiempo_actual = time.monotonic()

        primer_registro = ultimo_conteo_guardado is None

        cambio_conteo = (
            ultimo_conteo_guardado is not None
            and cantidad != ultimo_conteo_guardado
            and tiempo_actual - ultimo_registro >= 5
        )

        registro_periodico = (
            tiempo_actual - ultimo_registro >= 30
        )

        if not (
            primer_registro
            or cambio_conteo
            or registro_periodico
        ):
            return

        try:
            close_old_connections()

            RegistroConteo.objects.create(
                personas_detectadas=cantidad,
                capacidad_maxima=datos["capacidad"],
                porcentaje_ocupacion=datos["ocupacion"],
                estado_aforo=datos["estado"]
            )

            ultimo_conteo_guardado = cantidad
            ultimo_registro = tiempo_actual

        except Exception as error:
            print(
                "No se pudo guardar el registro:",
                error
            )

        finally:
            close_old_connections()


@require_POST
@csrf_protect
def analizar_imagen(request):
    archivo = request.FILES.get("imagen")

    if archivo is None:
        return JsonResponse(
            {"error": "No se recibió ninguna imagen."},
            status=400
        )

    # Limitar el tamaño de cada imagen a 2 MB.
    if archivo.size > 2 * 1024 * 1024:
        return JsonResponse(
            {"error": "La imagen es demasiado grande."},
            status=400
        )

    try:
        datos_imagen = np.frombuffer(
            archivo.read(),
            dtype=np.uint8
        )

        imagen = cv2.imdecode(
            datos_imagen,
            cv2.IMREAD_COLOR
        )

        if imagen is None:
            return JsonResponse(
                {"error": "No se pudo leer la imagen."},
                status=400
            )

        # YOLOv8 procesa una imagen a la vez.
        with bloqueo_detector:
            modelo = obtener_detector()

            imagen_procesada, cantidad = (
                modelo.detectar(imagen)
            )

        datos = calcular_estadisticas(cantidad)

        # Devolver los recuadros detectados.
        cajas = []

        # La imagen procesada ya contiene las
        # anotaciones realizadas por camara.py.
        correcto, buffer = cv2.imencode(
            ".jpg",
            imagen_procesada,
            [cv2.IMWRITE_JPEG_QUALITY, 75]
        )

        if not correcto:
            return JsonResponse(
                {"error": "No se pudo procesar la imagen."},
                status=500
            )

        import base64

        imagen_base64 = base64.b64encode(
            buffer.tobytes()
        ).decode("utf-8")

        datos["imagen"] = (
            "data:image/jpeg;base64,"
            + imagen_base64
        )

        guardar_registro(cantidad, datos)

        return JsonResponse(datos)

    except Exception as error:
        print("Error al analizar imagen:", error)

        return JsonResponse(
            {
                "error": (
                    "No se pudo analizar la imagen. "
                    "Revisa los registros del servidor."
                )
            },
            status=500
        )


def obtener_conteo(request):
    return JsonResponse(
        calcular_estadisticas(0)
    )
