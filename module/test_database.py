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


def test_dynamo_works():
    d = dynamo.DynamoDB()

    k = 'key'
    v = 'http://value-village.com'

    d.save(k, v)
    got = d.lookup(k)
    assert(got.get('long_url') == v)


def test_honors_create_date():
    d = dynamo.DynamoDB()

    k = 'key'
    v = 'http://value-village.com'
    create_date = datetime.datetime(year=2001, month=2, day=3, tzinfo=pytz.utc)

    d.save(k, v, create_date=create_date)
    got = d.lookup(k)
    assert(got.get('create_date') == str(create_date))
