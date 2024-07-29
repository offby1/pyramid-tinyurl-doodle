import logging
import urllib

import pytest
from app import views
from app.models import ShortenedURL
from django.conf import settings
from django.test import Client

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def set_debug_to_true(settings):
    settings.DEBUG = True


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
    assert views._fill_in_missing_url_components("hot/or/not") == "https://example.com/hot/or/not"


def test_rudybot_compatibility(rf):
    assert ShortenedURL.objects.count() == 0

    original = urllib.parse.unquote(
        "https%3A%2F%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2F",
        errors="strict",
    )
    request = rf.get(
        "/shorten-/",
        data={
            "input_url": original,
        },
        headers={
            "accept": "text/plain",
            "X-Forwarded-For": next(iter(settings.RUDYBOT_IP_ADDRESSES)),
        },
    )
    response = views.shorten(request)

    assert response.status_code == 200
    assert ShortenedURL.objects.count() == 1
    shorty = ShortenedURL.objects.first().short
    assert shorty == "kKc31g9Var"
    assert response.content == f"http://testserver/{shorty}/".encode()


def test_tells_rudybot_to_go_piss_up_a_rope_if_IP_address_is_wrong(
    rf,
):
    rudybot_ip_str = str(next(iter(settings.RUDYBOT_IP_ADDRESSES)))

    for header_dict, expected_status in (
        (
            {"X-Forwarded-For": rudybot_ip_str, "REMOTE_ADDR": "127.0.0.1"},
            200,
        ),  # typical case in prod
        ({"REMOTE_ADDR": "127.0.0.1"}, 200),  # me testing stuff, bypassing nginx
        ({"X-Forwarded-For": "66.249.66.13"}, 401),  # random person on Internet
        (
            {"X-Forwarded-For": "66.249.66.13", "REMOTE_ADDR": "127.0.0.1"},
            401,
        ),  # random person on Internet who somehow managed to forge the REMOTE_ADDR header
        (
            {"X-Forwarded-For": "66.249.66.13", "REMOTE_ADDR": rudybot_ip_str},
            401,
        ),  # similar
    ):
        request = rf.get(
            "/shorten-/",
            data={
                "input_url": "original",
            },
            headers=header_dict,
        )
        response = views.shorten(request)

        assert response.status_code == expected_status


@pytest.mark.parametrize(
    "url",
    [
        ("/",),
        ("/some-random-404",),
        ("/admin"),
    ],
)
def test_adds_x_robots_tag_header(url):
    c = Client()
    response = c.get(url)
    assert response.headers["X-Robots-Tag"] == "none"


def test_serves_robots_dot_txt():
    c = Client()
    response = c.get("/robots.txt")
    assert response.status_code == 200
    assert b"Disallow:" in response.content
