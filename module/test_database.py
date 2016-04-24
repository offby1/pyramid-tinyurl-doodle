import datetime

import database
import dynamo


import pytest
import pytz


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
    v = 'http://value-village.com'

    ddb.save(k, v)
    got = ddb.lookup(k)
    assert(got.get('long_url') == v)


def test_honors_create_date(ddb):
    k = 'key'
    v = 'http://value-village.com'
    create_date = datetime.datetime(year=2001, month=2, day=3, tzinfo=pytz.utc)

    ddb.save(k, v, create_date=create_date)
    got = ddb.lookup(k)
    assert(got.get('create_date') == str(create_date))
