from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    original = models.CharField(max_length=1024)
    short = models.CharField(max_length=settings.HASH_LENGTH, primary_key=True)

    def __str__(self):
        return f"{self.short} => {self.original[0:100]}"


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ["short", "original", "created_at"]
    list_filter = ["created_at"]
