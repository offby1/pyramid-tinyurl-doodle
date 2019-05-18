# 3rd-party
from pyramid import testing
import pytest

# Local
from tinyurl.auth import _captcha_info_is_valid, verify_request


@pytest.fixture
def mock_google(mocker):
    return mocker.patch('tinyurl.auth._do_the_google_thang')


@pytest.fixture
def dummy_request():
    r = testing.DummyRequest(params={'g-recaptcha-response': 'yeah yeah whatever'})
    r.client_addr = '1.2.3.4'
    return r


def test_missing_g_recaptcha_response_URL_parameter():
    request = testing.DummyRequest()

    assert not _captcha_info_is_valid(request)


def test_Google_says_drop_dead(mock_google, dummy_request):
    mock_google.return_value = False
    assert not _captcha_info_is_valid(dummy_request)


def test_Google_says_eva_thang_funky(mock_google, dummy_request):
    mock_google.return_value = True
    assert _captcha_info_is_valid(dummy_request)


def test_we_only_do_the_google_roundtrip_once(mock_google, dummy_request):
    mock_google.return_value = True

    assert verify_request(dummy_request)
    assert verify_request(dummy_request)

    assert len(mock_google.call_args_list) == 1
