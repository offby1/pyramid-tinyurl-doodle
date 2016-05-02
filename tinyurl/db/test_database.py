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

    for k in (k1, k2):
        ddb.delete(k)

    ddb.add_if_not_present(k1, v1)
    ddb.add_if_not_present(k2, v2)

    assert(ddb.lookup(k1).get('long_url') == v1)
    assert(ddb.lookup(k2).get('long_url') == v2)

    ddb.delete(k1)
    with pytest.raises(KeyError):
        ddb.lookup(k1)
    assert(ddb.lookup(k2).get('long_url') == v2)


def test_get_all_returns_items_ordered_newest_first(ddb):
    def _tuple_to_dict(t):
        return {'human_hash': t[0],
                'long_url': t[1],
                'create_date': str(t[2])}
    row1 = ('key1', 'value1')
    row2 = ('key2', 'value2')
    row3 = ('key3', 'value3')
    for (k, v) in (row1, row3, row2) :
        ddb.add_if_not_present(k, v)

    all = ddb.get_all()
    timestamps = [item['create_date'] for item in all if item['human_hash'] in ('key1', 'key2', 'key3')]

    assert timestamps == sorted(timestamps, reverse=True)

def test_batch_writer(ddb):
    bulk_data = [
        {'human_hash': 'key one', 'long_url': 'value one'},
        {'human_hash': 'key two', 'long_url': 'value two'},
    ]
    for d in bulk_data:
        ddb.delete(d['human_hash'])
    ddb.batch_add_key_value_pairs(bulk_data)
    for d in bulk_data:
        got = ddb.lookup(d['human_hash'])
        assert(got == d)
