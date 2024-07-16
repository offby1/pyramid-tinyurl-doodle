from django.urls import path, register_converter

from . import converters, views

register_converter(converters.HashConverter, "hh")

urlpatterns = [
    path("", views.homepage),
    path("robots.txt", views.robots_dot_txt, name="robots.txt"),
    path("<hh:short>/", views.lengthen, name="lengthen"),
    path("shorten-/", views.shorten, name="shorten"),
]
