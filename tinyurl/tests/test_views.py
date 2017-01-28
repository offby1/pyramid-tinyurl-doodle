# 3rd-party
from pyramid import testing
import pytest

# Local
from tinyurl import views
from tinyurl.helpers import EtagMemoizer

etag_cache_thing = EtagMemoizer()


@pytest.fixture
def null_renderer(mocker):
    return mocker.patch('tinyurl.views.render_html_or_text',
                        side_effect=lambda request, values:
                        (str(values), 'text/shmext'))


@pytest.fixture
def request():
    rv = testing.DummyRequest()
    rv.etag_cache_thing = etag_cache_thing
    return rv


def test_display_captcha_when_not_authed(null_renderer, request):
    views.home_GET(request)
    (req, dict_), _ = null_renderer.call_args_list[0]
    assert dict_['display_captcha']


def test_no_captcha_when_authed(null_renderer, request):
    request.session['authenticated'] = True
    views.home_GET(request)
    (req, dict_), _ = null_renderer.call_args_list[0]
    assert not dict_['display_captcha']
