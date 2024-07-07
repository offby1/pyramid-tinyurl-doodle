import app.views
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", app.views.homepage),
    path("admin/", admin.site.urls),
    path("lengthen/<short>", app.views.lengthen, name="lengthen"),
    path("shorten-/", app.views.shorten, name="shorten"),
] + debug_toolbar_urls()
