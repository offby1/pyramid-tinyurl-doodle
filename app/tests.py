import urllib

import pytest
from app import views
from app.models import ShortenedURL
from django.test import Client

pytestmark = pytest.mark.django_db


def test_short_link_on_homepage_redirects_to_original_url(settings):
    c = Client()
    original = "https://my.what.a.long.url/you/have/grandma"
    settings.RECAPTCHA_BACKDOOR = True
    post_response = c.post(
        "/shorten-/",
        data={
            "original": original,
        },
    )
    assert post_response.status_code == 201
    short = ShortenedURL.objects.get(original=original).short
    lengthen_url = post_response.headers["Location"]
    assert short in lengthen_url
    homepage_response = c.get("/").content.decode()
    assert f"""<a href="{lengthen_url}">{short}</a>""" in homepage_response

    lengthen_response = c.get(lengthen_url)
    assert lengthen_response.status_code in (302, 303)
    assert lengthen_response.url == original


def test_failed_recaptcha_gets_us_a_401():
    c = Client()
    original = "https://my.what.a.long.url/you/have/grandma"
    response = c.post(
        "/shorten-/",
        data={
            "original": original,
        },
    )
    assert response.status_code == 401


def test_fills_in_missing_url_components():
    assert views._fill_in_missing_url_components("wat") == "https://example.com/wat"
    assert (
        views._fill_in_missing_url_components("hot/or/not")
        == "https://example.com/hot/or/not"
    )


def test_rudybot_compatibility():
    assert ShortenedURL.objects.count() == 0

    c = Client()
    original = urllib.parse.unquote(
        "https%3A%2F%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2F",
        errors="strict",
    )
    response = c.get(
        "/shorten-/",
        data={
            "input_url": original,
        },
        headers={
            "accept": "text/plain",
        },
    )
    assert response.status_code == 200
    assert ShortenedURL.objects.count() == 1
    shorty = ShortenedURL.objects.first().short
    assert shorty == "kKc31g9Var"
