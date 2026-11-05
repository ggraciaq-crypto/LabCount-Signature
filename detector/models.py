
from django.db import models


class RegistroConteo(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    personas_detectadas = models.PositiveIntegerField()
    capacidad_maxima = models.PositiveIntegerField(default=10)
    porcentaje_ocupacion = models.FloatField()
    estado_aforo = models.CharField(max_length=30)

    class Meta:
        db_table = "registro_conteo"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.fecha_hora} - {self.personas_detectadas} personas"
