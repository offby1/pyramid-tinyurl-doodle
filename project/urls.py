import app.urls
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(app.urls)),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
