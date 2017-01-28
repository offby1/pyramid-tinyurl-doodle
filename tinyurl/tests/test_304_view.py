# 3rd-party
import arrow
from pyramid import testing
import pytest

# Local
from tinyurl import views
from tinyurl.helpers import EtagMemoizer

etag_cache_thing = EtagMemoizer()


@pytest.fixture
def request(headers=None):
    rv = testing.DummyRequest(headers=headers)
    rv.etag_cache_thing = etag_cache_thing
    return rv


def test_304():
    # stop the clock so that we can predict the return values from _304_test
    now = arrow.get('2011-01-01')

    request1 = request()
    resp1 = views._304_test(request1, now=now)
    print("test sez: resp1 =", repr(str(resp1)))
    ETag1 = resp1.headers.get('ETag', '')

    request2 = request(headers={'If-None-Match': 'frotzlplotz' + ETag1})
    resp2 = views._304_test(request2, now=now)
    print("test sez: resp2 =", repr(str(resp2)))

    assert resp2.status_code == 200
    ETag2 = resp2.headers['ETag']
    assert ETag2 == ETag1

    request3 = request(headers={'If-None-Match': ETag1})
    resp3 = views._304_test(request3, now=now)
    print("test sez: resp3 =", repr(str(resp3)))

    assert resp3.status_code == 304
    assert resp3.body == b''
