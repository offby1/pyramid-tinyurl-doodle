from app.models import ShortenedURL
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def lengthen(request, short=None):
    obj = get_object_or_404(ShortenedURL, short=short)
    return HttpResponse(obj.original)


def shorten(request, original):
    short = f"xyzzy{len(original)}"
    obj, created = ShortenedURL.objects.get_or_create(
        short=short,
        original=original,
    )
    return HttpResponse(short)
