from django.urls import path, register_converter

from . import converters, views

register_converter(converters.HashConverter, "hh")

urlpatterns = [
    path("", views.homepage),
    path("<hh:short>/", views.lengthen, name="lengthen"),
    path("shorten-/", views.shorten, name="shorten"),
]
