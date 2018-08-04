import mock

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
    mock_database = mock.Mock(name='database')
    mock_database.table.item_count = 123

    return testing.DummyRequest(database=mock_database)


def test_display_captcha_when_not_authed(null_renderer, dummy_request):
    resp = views.home_GET(dummy_request)
    assert resp['display_captcha']


def test_no_captcha_when_authed(null_renderer, dummy_request):
    dummy_request.session['authenticated'] = True
    resp = views.home_GET(dummy_request)
    assert not resp['display_captcha']


def test_response_type_defaults_to_text(dummy_request):
    assert views._determine_response_type(dummy_request) == views.ResponseType.TEXT


def test_HTML_accept_header(null_renderer, dummy_request):
    dummy_request.headers['Accept'] = 'text/html'

    assert views._determine_response_type(dummy_request) == views.ResponseType.HTML


def test_doesnt_gack_on_invalid_accept_header(dummy_request):
    dummy_request.headers.update({'Accept': None})

    assert views._determine_response_type(dummy_request) == views.ResponseType.TEXT
