from django.conf import settings
from django.contrib import admin
from django.db import models


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.CharField(max_length=1024)
    short = models.CharField(max_length=settings.HASH_LENGTH, primary_key=True)

    def __str__(self):
        return f"{self.short} => {self.original[0:100]}"


admin.site.register(ShortenedURL)
