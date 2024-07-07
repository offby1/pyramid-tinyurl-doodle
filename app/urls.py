import app.views
from django.urls import path

urlpatterns = [
    path("", app.views.homepage),
    path("lengthen/<short>", app.views.lengthen, name="lengthen"),
    path("shorten-/", app.views.shorten, name="shorten"),
]
