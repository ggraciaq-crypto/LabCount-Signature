
from django.contrib import admin
from django.urls import path

from detector import views


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        views.inicio,
        name="inicio"
    ),

    path(
        "analizar/",
        views.analizar_imagen,
        name="analizar_imagen"
    ),

    path(
        "conteo/",
        views.obtener_conteo,
        name="obtener_conteo"
    ),
]
