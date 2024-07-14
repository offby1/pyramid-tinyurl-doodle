import binascii
import hashlib
import logging
import urllib.parse

import requests
from app.forms import ShortenForm
from app.models import ShortenedURL
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


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

    # This conversion must be kept in sync with .converters.HashConverter
    human_hash_bytes = binascii.b2a_base64(binary_hash)
    human_hash_bytes = human_hash_bytes.replace(b"+", b"").replace(b"/", b"")[
        : settings.HASH_LENGTH
    ]

    return human_hash_bytes.decode("utf-8")


def _response_content_type(request):
    if request.accepts("text/html"):
        return "text/html"

    return "text/plain"


def maybe_render(request, context=None, status=None):
    if context is None:
        context = {}

    content_type = _response_content_type(request)
    if content_type != "text/html":
        return HttpResponse(
            context.get("short_url", ""),
            content_type=content_type,
            status=200,
        )

    gitlab_home_page = "https://gitlab.com/offby1/teensy/-/"

    context["approximate_table_size"] = ShortenedURL.objects.count()
    context["display_captcha"] = "short" not in context
    context["form"] = (
        ShortenForm(request.POST) if request.method == "POST" else ShortenForm()
    )
    context["recent_entries"] = ShortenedURL.objects.order_by("-created_at")[:10]
    context["this_commit_url"] = f"{gitlab_home_page}commit/{settings.GIT_INFO}"

    return render(request, "homepage.html", context=context, status=status)


def _do_the_google_thang(request, g_captcha_response):
    response = requests.post(
        url="https://www.google.com/recaptcha/api/siteverify",
        data=dict(
            secret=settings.RECAPTCHA_SECRET,
            response=g_captcha_response,
            remoteip=request.META[
                "REMOTE_ADDR"  # request.headers["X-Forwarded-For"] might work too, if we're behind nginx and I've
                # configured it to add that header
            ],
        ),
    ).json()
    logger.debug("Google's pronouncement: %s", response)
    return response["success"]


def _check_recaptcha_response(request):
    post_data = request.POST
    if settings.RECAPTCHA_BACKDOOR:
        logger.debug(f"{settings.RECAPTCHA_BACKDOOR=} so returning True")
        return True

    if "g-recaptcha-response" not in post_data:
        logger.debug(f"{post_data=} has no g-recaptcha-response, returning False")
        return False

    g_captcha_response = post_data["g-recaptcha-response"]
    if not g_captcha_response:
        logger.debug(f"{g_captcha_response=} is false-y; returning False")

    return _do_the_google_thang(request, g_captcha_response)


def _shorten_POST(request):
    if not _check_recaptcha_response(request):
        return TemplateResponse(
            request,
            status=401,
            template="recaptcha_fail.html",
        )

    form = ShortenForm(request.POST)
    if not form.is_valid():
        return maybe_render(request)

    original = form.cleaned_data["original"]
    short = _enhashify(original)
    ShortenedURL.objects.get_or_create(
        short=short,
        original=original,
    )

    response = maybe_render(
        request,
        context={
            "short": short,
        },
        status=201,
    )
    response.headers["Location"] = reverse("lengthen", kwargs=dict(short=short))
    return response


# Backwards compatibility for rudybot
def _shorten_GET(request):
    original = request.GET["input_url"]

    short = _enhashify(original)
    ShortenedURL.objects.get_or_create(
        short=short,
        original=original,
    )

    response = HttpResponse(
        original,
        headers={"Content-Type": "text/plain"},
        status=200,
    )

    return response


@require_http_methods(["GET", "POST"])
def shorten(request):
    if request.method == "POST":
        return _shorten_POST(request)

    return _shorten_GET(request)


def homepage(request):
    return maybe_render(request)
