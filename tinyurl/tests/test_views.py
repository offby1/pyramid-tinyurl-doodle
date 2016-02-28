# 3rd-party
from pyramid import testing
import pytest

# Local
from tinyurl import views


@pytest.fixture
def null_renderer(mocker):
    return mocker.patch('tinyurl.views.render', side_effect=lambda request, values: values)


@pytest.fixture
def request():
    return testing.DummyRequest()


def test_display_captcha_when_not_authed(null_renderer, request):
    resp = views.home_GET(request)
    assert resp['display_captcha']


def test_no_captcha_when_authed(null_renderer, request):
    request.session['authenticated'] = True
    resp = views.home_GET(request)
    assert not resp['display_captcha']
