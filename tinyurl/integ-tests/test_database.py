import datetime

# 3rd-party
import pytest

# Local
from tinyurl.db import dynamo


@pytest.fixture
def ddb():
    return dynamo.DynamoDB('hashes-test', 'create_day-create_date-index')


def test_dynamo_works(ddb):
    k = 'key'
    v = 'http://valuevillage.com'

    ddb.delete(k)
    ddb.add_if_not_present(k, v)
    got = ddb.lookup(k)
    assert got.get('long_url') == v


def test_add_if_not_present(ddb):
    k = 'key'
    v1 = 'http://valuevillage.com'
    v2 = 'some other value'

    ddb.delete(k)
    ddb.add_if_not_present(k, v1)
    ddb.add_if_not_present(k, v2)
    got = ddb.lookup(k)
    assert got.get('long_url') == v1


def test_delete(ddb):
    k1 = 'key one'
    v1 = 'http://valuevillage.com'

    k2 = 'key two'
    v2 = 'some other value'

    for k in (k1, k2):
        ddb.delete(k)

    ddb.add_if_not_present(k1, v1)
    ddb.add_if_not_present(k2, v2)

    assert ddb.lookup(k1).get('long_url') == v1
    assert ddb.lookup(k2).get('long_url') == v2

    ddb.delete(k1)
    with pytest.raises(KeyError):
        ddb.lookup(k1)
    assert ddb.lookup(k2).get('long_url') == v2


def test_get_all_returns_items_ordered_newest_first(ddb):
    def _tuple_to_dict(t):
        return {'human_hash': t[0], 'long_url': t[1], 'create_date': str(t[2])}

    row1 = ('key1', 'value1')
    row2 = ('key2', 'value2')
    row3 = ('key3', 'value3')
    for (k, v) in (row1, row3, row2):
        ddb.add_if_not_present(k, v)

    all = ddb.get_all()
    timestamps = [
        item['create_date']
        for item in all
        if item['human_hash'] in ('key1', 'key2', 'key3')
    ]

    assert timestamps == sorted(timestamps, reverse=True)


def test_get_one_days_hashes(ddb):
    rows = [
        {
            'human_hash': 'one',
            'long_url': 'meh',
            'create_day': '2017-01-12',
            'create_date': '2017-01-12T12:00:00Z',
        },
        {
            'human_hash': 'two',
            'long_url': 'meh',
            'create_day': '2017-01-11',
            'create_date': '2017-01-11T18:00:00Z',
        },
        {
            'human_hash': 'three',
            'long_url': 'meh',
            'create_day': '2017-01-11',
            'create_date': '2017-01-11T06:00:00Z',
        },
        {
            'human_hash': 'four',
            'long_url': 'meh',
            'create_day': '2017-01-10',
            'create_date': '2017-01-10T12:00:00Z',
        },
    ]
    for item in rows:
        ddb.table.update_item(
            Key={'human_hash': item['human_hash']},
            TableName=ddb.table.name,
            UpdateExpression=(
                'set long_url = :long_url'
                ', create_day = :create_day'
                ', create_date = :create_date'
            ),
            ExpressionAttributeValues={
                ':long_url': item['long_url'],
                ':create_day': item['create_day'],
                ':create_date': item['create_date'],
            },
        )

    assert (
        ddb.get_one_days_hashes(datetime.date(year=2017, month=1, day=12)) == rows[0:1]
    )
    assert (
        ddb.get_one_days_hashes(datetime.date(year=2017, month=1, day=11)) == rows[1:3]
    )
    assert (
        ddb.get_one_days_hashes(
            datetime.date(year=2017, month=1, day=11),
            later_than=datetime.datetime(year=2017, month=1, day=11, hour=6),
        )
        == rows[1:3]
    )
