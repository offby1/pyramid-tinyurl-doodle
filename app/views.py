import binascii
import hashlib

from app.models import ShortenedURL
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def lengthen(request, short=None):
    obj = get_object_or_404(ShortenedURL, short=short)
    return HttpResponse(obj.original)


def _enhashify(long_url):
    if isinstance(long_url, str):
        long_url_bytes = long_url.encode("utf-8")
    elif isinstance(long_url, bytes):
        long_url_bytes = long_url
    else:
        raise Exception(f"{long_url} doesn't seem to be a string, or a bytes")

    hash_object = hashlib.sha256(long_url_bytes)
    binary_hash = hash_object.digest()
    human_hash_bytes = binascii.b2a_base64(binary_hash)
    human_hash_bytes = human_hash_bytes.replace(b"+", b"").replace(b"/", b"")[:10]
    return human_hash_bytes.decode("utf-8")


def shorten(request, original):
    short = _enhashify(original)
    obj, created = ShortenedURL.objects.get_or_create(
        short=short,
        original=original,
    )
    return HttpResponse(short)


def homepage(request):
    return render(request, "homepage.html")
