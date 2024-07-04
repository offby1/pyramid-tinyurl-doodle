import pytest
from app.models import ShortenedURL
from django.test import Client

# Create your tests here.


pytestmark = pytest.mark.django_db


def test_wat():
    # create one entry
    ShortenedURL.objects.create(
        short="xyzzy",
        original="https://my.what.a.long.url/you/have/grandma",
    )
    # fetch entry
    c = Client()
    response = c.get("/lengthen/xyzzy")
    assert "https://my.what.a.long.url/you/have/grandma" in response.content.decode()
