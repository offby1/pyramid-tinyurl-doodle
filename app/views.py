import binascii
import hashlib
import urllib.parse

from app.forms import ShortenForm
from app.models import ShortenedURL
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods


def _fill_in_missing_url_components(url_string):
    parsed = urllib.parse.urlparse(url_string)

    if not parsed.scheme:
        parsed = parsed._replace(scheme="https")

    if not parsed.netloc:
        parsed = parsed._replace(netloc="example.com")

    return urllib.parse.urlunparse(parsed)


def lengthen(request, short=None):
    obj = get_object_or_404(ShortenedURL, short=short)
    return HttpResponseRedirect(_fill_in_missing_url_components(obj.original))


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


def _response_content_type(request):
    if request.accepts("text/html"):
        return "text/html"

    return "text/plain"


def maybe_render(request, context=None):
    if context is None:
        context = {}

    content_type = _response_content_type(request)
    if content_type != "text/html":
        return HttpResponse(
            context.get("short_url", ""),
            content_type=content_type,
            status_code=200,
        )

    gitlab_home_page = "https://gitlab.com/offby1/teensy/-/"

    context["approximate_table_size"] = ShortenedURL.objects.count()
    context["display_captcha"] = "short" not in context
    context["form"] = (
        ShortenForm(request.POST) if request.method == "POST" else ShortenForm()
    )
    context["recent_entries"] = ShortenedURL.objects.order_by("-created_at")[:10]
    context["this_commit_url"] = f"{gitlab_home_page}commit/{settings.GIT_INFO}"

    return render(request, "homepage.html", context=context)


@require_http_methods(["GET", "POST"])
def shorten(request):
    if request.method == "POST":
        form = ShortenForm(request.POST)
        if form.is_valid():
            original = form.cleaned_data["original"]
            short = _enhashify(original)
            ShortenedURL.objects.get_or_create(
                short=short,
                original=original,
            )

            return maybe_render(
                request,
                context={
                    "short": short,
                },
            )

    return maybe_render(request)


def homepage(request):
    return maybe_render(request)
