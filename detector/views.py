
import cv2
import threading
import time

from django.db import close_old_connections
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .camara import DetectorPersonas
from .models import RegistroConteo


total_personas = 0
bloqueo = threading.Lock()


def inicio(request):
    return render(request, "detector/inicio.html")


def generar_video():
    global total_personas

    camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camara.isOpened():
        return

    detector = DetectorPersonas()
    ultimo_conteo_guardado = None
    ultimo_registro = 0

    try:
        while True:
            correcto, imagen = camara.read()

            if not correcto:
                break

            imagen, cantidad = detector.detectar(imagen)

            with bloqueo:
                total_personas = cantidad

            tiempo_actual = time.monotonic()

            cambio_conteo = (
                ultimo_conteo_guardado is not None
                and cantidad != ultimo_conteo_guardado
                and tiempo_actual - ultimo_registro >= 5
            )

            registro_periodico = (
                tiempo_actual - ultimo_registro >= 30
            )

            primer_registro = ultimo_conteo_guardado is None

            if primer_registro or cambio_conteo or registro_periodico:
                capacidad = 10
                ocupacion = round((cantidad / capacidad) * 100)

                if cantidad >= capacidad:
                    estado = "Aforo completo"
                else:
                    estado = "Seguro"

                try:
                    close_old_connections()

                    RegistroConteo.objects.create(
                        personas_detectadas=cantidad,
                        capacidad_maxima=capacidad,
                        porcentaje_ocupacion=ocupacion,
                        estado_aforo=estado
                    )

                    ultimo_conteo_guardado = cantidad
                    ultimo_registro = tiempo_actual

                except Exception:
                    pass

                finally:
                    close_old_connections()

            correcto, buffer = cv2.imencode(".jpg", imagen)

            if not correcto:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )

    finally:
        camara.release()

        with bloqueo:
            total_personas = 0


def video_camara(request):
    return StreamingHttpResponse(
        generar_video(),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )


def obtener_conteo(request):
    with bloqueo:
        cantidad = total_personas

    capacidad = 10
    ocupacion = round((cantidad / capacidad) * 100)

    if cantidad >= capacidad:
        estado = "Aforo completo"
    else:
        estado = "Seguro"

    return JsonResponse({
        "personas": cantidad,
        "capacidad": capacidad,
        "ocupacion": ocupacion,
        "estado": estado
    })
