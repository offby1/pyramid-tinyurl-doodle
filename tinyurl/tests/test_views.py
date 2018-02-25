# 3rd-party
from pyramid import testing
import pytest

# Local
from tinyurl import views


@pytest.fixture
def null_renderer(mocker):
    return mocker.patch('tinyurl.views.render',
                        side_effect=lambda request, values: values)


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()


def test_display_captcha_when_not_authed(null_renderer, dummy_request):
    resp = views.home_GET(dummy_request)
    assert resp['display_captcha']


def test_no_captcha_when_authed(null_renderer, dummy_request):
    dummy_request.session['authenticated'] = True
    resp = views.home_GET(dummy_request)
    assert not resp['display_captcha']
