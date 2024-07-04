from django.contrib import admin
from django.db import models

# Create your models here.


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.CharField(max_length=1024)
    short = models.CharField(max_length=12, primary_key=True)


admin.site.register(ShortenedURL)