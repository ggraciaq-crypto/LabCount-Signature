
from django.test import TestCase
from django.urls import reverse

from .models import RegistroConteo


class PruebasLabCount(TestCase):

    def test_pagina_principal(self):
        respuesta = self.client.get(reverse("inicio"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(
            respuesta,
            "detector/inicio.html"
        )

    def test_conteo_inicial(self):
        respuesta = self.client.get(reverse("obtener_conteo"))

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.json()

        self.assertIn("personas", datos)
        self.assertEqual(datos["capacidad"], 10)
        self.assertEqual(
            datos["ocupacion"],
            round(datos["personas"] / 10 * 100)
        )

    def test_estado_del_aforo(self):
        respuesta = self.client.get(reverse("obtener_conteo"))
        datos = respuesta.json()

        if datos["personas"] >= datos["capacidad"]:
            self.assertEqual(
                datos["estado"],
                "Aforo completo"
            )
        else:
            self.assertEqual(
                datos["estado"],
                "Seguro"
            )

    def test_guardar_registro(self):
        registro = RegistroConteo.objects.create(
            personas_detectadas=2,
            capacidad_maxima=10,
            porcentaje_ocupacion=20,
            estado_aforo="Seguro"
        )

        self.assertEqual(registro.personas_detectadas, 2)
        self.assertEqual(registro.porcentaje_ocupacion, 20)
        self.assertEqual(registro.estado_aforo, "Seguro")

    def test_consultar_registros(self):
        RegistroConteo.objects.create(
            personas_detectadas=1,
            capacidad_maxima=10,
            porcentaje_ocupacion=10,
            estado_aforo="Seguro"
        )

        RegistroConteo.objects.create(
            personas_detectadas=3,
            capacidad_maxima=10,
            porcentaje_ocupacion=30,
            estado_aforo="Seguro"
        )

        self.assertEqual(
            RegistroConteo.objects.count(),
            2
        )
