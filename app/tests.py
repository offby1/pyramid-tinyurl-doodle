import pytest
from app.models import ShortenedURL
from django.test import Client

# Create your tests here.


pytestmark = pytest.mark.django_db


def test_wat():
    # create one entry via DB
    ShortenedURL.objects.create(
        short="xyzzy",
        original="https://my.what.a.long.url/you/have/grandma",
    )
    # fetch entry
    c = Client()
    response = c.get("/lengthen/xyzzy")
    assert "https://my.what.a.long.url/you/have/grandma" in response.content.decode()


def test_snot():
    # Create one entry via web
    c = Client()
    some_url = "https://my.what.a.long.url/you/have/grandma"
    response = c.post("/shorten/", data={"original": some_url})
    # fetch entry
    assert response.status_code in (200, 201)
    short = response.content.decode()

    response = c.get(f"/lengthen/{short}")
    assert response.status_code == 200
    assert some_url in response.content.decode()


def test_short_link_on_homepage_gets_properly_expanded():
    c = Client()
    some_url = "https://my.what.a.long.url/you/have/grandma"
    c.post("/shorten/", data={"original": some_url})
    short = ShortenedURL.objects.get(original=some_url).short

    homepage_response = c.get("/").content.decode()
    assert f"""<a href="/lengthen/{short}">{short}</a>""" in homepage_response
