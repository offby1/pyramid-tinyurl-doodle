import pytest
from app.models import ShortenedURL
from django.test import Client

pytestmark = pytest.mark.django_db


def test_short_link_on_homepage_goes_to_lengthen_url():
    c = Client()
    some_url = "https://my.what.a.long.url/you/have/grandma"
    c.post("/shorten/", data={"original": some_url})
    short = ShortenedURL.objects.get(original=some_url).short

    homepage_response = c.get("/").content.decode()
    lengthen_url = f"/lengthen/{short}"
    assert f"""<a href="{lengthen_url}">{short}</a>""" in homepage_response

    lengthen_response = c.get(lengthen_url)
    assert lengthen_response.status_code in (302, 303)
    assert lengthen_response.url == some_url
