# Core
import datetime
import uuid

# 3rd-party
import pytest
import pytz

# Local
from . import database
from . import dynamo


def test_it_really_is_abstract ():
    class MissingRequiredMethods(database.DatabaseMeta):
        pass

    with pytest.raises(TypeError):
        MissingRequiredMethods()


@pytest.fixture
def ddb():
    return dynamo.DynamoDB()


def test_dynamo_works(ddb):
    k = 'key'
    v = 'http://valuevillage.com'

    ddb.delete(k)
    ddb.add_if_not_present(k, v)
    got = ddb.lookup(k)
    assert(got.get('long_url') == v)


def test_add_if_not_present(ddb):
    k = 'key'
    v1 = 'http://valuevillage.com'
    v2 = 'some other value'

    ddb.delete(k)
    ddb.add_if_not_present(k, v1)
    ddb.add_if_not_present(k, v2)
    got = ddb.lookup(k)
    assert(got.get('long_url') == v1)


def test_delete(ddb):
    k1 = 'key one'
    v1 = 'http://valuevillage.com'

    k2 = 'key two'
    v2 = 'some other value'

    ddb.add_if_not_present(k1, v1)
    ddb.add_if_not_present(k2, v2)

    assert(ddb.lookup(k1).get('long_url') == v1)
    assert(ddb.lookup(k2).get('long_url') == v2)

    ddb.delete(k1)
    with pytest.raises(KeyError):
        ddb.lookup(k1)
    assert(ddb.lookup(k2).get('long_url') == v2)


def test_honors_create_date(ddb):
    k = str(uuid.uuid4())
    v = 'http://valuevillage.com'
    create_date = datetime.datetime(year=2001, month=2, day=3, tzinfo=pytz.utc)

    ddb.add_if_not_present(k, v, create_date=create_date)
    got = ddb.lookup(k)
    assert(got.get('create_date') == str(create_date))

    # Once again just to be sure ...
    import time
    time.sleep(1)
    ddb.add_if_not_present(k, v)
    got = ddb.lookup(k)
    assert(got.get('create_date') == str(create_date))


def test_get_all_returns_items_ordered_newest_first(ddb):
    def _tuple_to_dict(t):
        return {'human_hash': t[0],
                'long_url': t[1],
                'create_date': str(t[2])}
    row1 = ('key1', 'value1', datetime.datetime(year=2001, month=1, day=1, tzinfo=pytz.utc))
    row2 = ('key2', 'value2', datetime.datetime(year=2002, month=2, day=2, tzinfo=pytz.utc))
    row3 = ('key3', 'value3', datetime.datetime(year=2003, month=3, day=3, tzinfo=pytz.utc))
    for (k, v, create_date) in (row1, row3, row2) :
        ddb.add_if_not_present(k, v, create_date=create_date)

    all = ddb.get_all()
    relevant = [item for item in all if item['human_hash'] in ('key1', 'key2', 'key3')]

    assert relevant == [_tuple_to_dict(r) for r in (row3, row2, row1)]
