import binascii
import hashlib

from app.forms import ShortenForm
from app.models import ShortenedURL
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods


def lengthen(request, short=None):
    obj = get_object_or_404(ShortenedURL, short=short)
    return HttpResponseRedirect(obj.original)


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
    human_hash_bytes = human_hash_bytes.replace(b"+", b"").replace(b"/", b"")[
        : settings.HASH_LENGTH
    ]
    return human_hash_bytes.decode("utf-8")


@require_http_methods(["POST"])
def shorten(request):
    form = ShortenForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect("/")

    original = form.cleaned_data["original"]

    short = _enhashify(original)
    obj, created = ShortenedURL.objects.get_or_create(
        short=short,
        original=original,
    )
    return HttpResponse(short)


def homepage(request):
    context = {}
    context["approximate_table_size"] = ShortenedURL.objects.count()
    context["recent_entries"] = ShortenedURL.objects.order_by("-created_at")[:10]
    context["form"] = ShortenForm()
    return render(request, "homepage.html", context=context)
