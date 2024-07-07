import pytest
from app import views
from app.models import ShortenedURL
from django.test import Client

pytestmark = pytest.mark.django_db


def test_short_link_on_homepage_redirects_to_original_url():
    c = Client()
    original = "https://my.what.a.long.url/you/have/grandma"
    c.get("/shorten-/", data={"original": original})
    short = ShortenedURL.objects.get(original=original).short

    homepage_response = c.get("/").content.decode()
    lengthen_url = f"/lengthen/{short}"
    assert f"""<a href="{lengthen_url}">{short}</a>""" in homepage_response

    lengthen_response = c.get(lengthen_url)
    assert lengthen_response.status_code in (302, 303)
    assert lengthen_response.url == original


@pytest.mark.skip(reason="I haven't figured out how to write i")
def test_clicking_submit_button_leaves_you_on_updated_homepage():
    assert False, "this would be failing if I knew how to write it :-)"


def test_fills_in_missing_url_components():
    assert views._fill_in_missing_url_components("wat") == "https://example.com/wat"
    assert (
        views._fill_in_missing_url_components("hot/or/not")
        == "https://example.com/hot/or/not"
    )
