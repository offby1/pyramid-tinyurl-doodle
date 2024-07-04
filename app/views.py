from app.models import ShortenedURL
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def lengthen(request, short=None):
    obj = get_object_or_404(ShortenedURL, short=short)
    return HttpResponse(obj.original)


def shorten(request, original):
    return HttpResponse("xyzzy")
