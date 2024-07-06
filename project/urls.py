import app.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", app.views.homepage),
    path("admin/", admin.site.urls),
    path("lengthen/<short>", app.views.lengthen, name="lengthen"),
    path("shorten-/", app.views.shorten, name="shorten"),
]
