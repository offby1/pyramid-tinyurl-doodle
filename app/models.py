from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    original = models.CharField(max_length=1024)
    short = models.CharField(max_length=settings.HASH_LENGTH, primary_key=True)

    @admin.display(description="short", ordering="short")
    def fixed_font_short(self):
        return format_html(
            "<tt>{}</tt>",
            self.short,
        )

    @admin.display(description="created_at", ordering="created_at")
    def iso_timestamp_created_at(self):
        return format_html(
            "<tt>{}</tt>",
            self.created_at.isoformat(),
        )

    def __str__(self):
        return f"{self.short} => {self.original[0:100]}"


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ["fixed_font_short", "original", "iso_timestamp_created_at"]
    list_filter = ["created_at"]
