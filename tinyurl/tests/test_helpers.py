import datetime
from functools import partial

import mock
import pytest
import pytz
from tinyurl.helpers import n_most_recent


@pytest.fixture
def db():
    return [
        {
            'create_day': '1968-05-17',
            'create_date': '1968-05-17T16:00:00Z',
            'human_hash': '8EIIU6',
        },
        {
            'create_day': '1968-05-17',
            'create_date': '1968-05-17T14:00:00Z',
            'human_hash': 'RR3F4F',
        },
        {
            'create_day': '1968-05-17',
            'create_date': '1968-05-17T12:00:00Z',
            'human_hash': 'Y87T8Q',
        },
        {
            'create_day': '1968-05-17',
            'create_date': '1968-05-17T10:00:00Z',
            'human_hash': 'MRI7QM',
        },
        {
            'create_day': '1968-05-16',
            'create_date': '1968-05-16T16:00:00Z',
            'human_hash': 'D3JKUR',
        },
        {
            'create_day': '1968-05-16',
            'create_date': '1968-05-16T14:00:00Z',
            'human_hash': 'V8WS2O',
        },
        {
            'create_day': '1968-05-16',
            'create_date': '1968-05-16T12:00:00Z',
            'human_hash': '9OW3YR',
        },
        {
            'create_day': '1968-05-16',
            'create_date': '1968-05-16T10:00:00Z',
            'human_hash': '6FGBH9',
        },
        {
            'create_day': '1968-05-15',
            'create_date': '1968-05-15T14:00:00Z',
            'human_hash': 'ZQMHLL',
        },
        {
            'create_day': '1968-05-15',
            'create_date': '1968-05-15T12:00:00Z',
            'human_hash': '715DK6',
        },
    ]


def fetch_day(db, dt, later_than=None):
    for row in db:
        if later_than and (later_than.isoformat() >= row['create_date']):
            return

        if row['create_day'] == dt.isoformat():
            yield row


now = datetime.datetime(year=1968, month=5, day=17)


def test_n_most_recent(db):
    gotten = list(n_most_recent(now, partial(fetch_day, db), num_items=10, days_back=4))
    assert len(gotten) == 10


def test_n_most_recent_honors_later_than(db):
    mock_fetcher = mock.Mock()
    mock_fetcher.side_effect = lambda dt, later_than=None: fetch_day(
        db, dt, later_than=later_than
    )
    later_than = datetime.datetime(year=1968, month=5, day=16, hour=12, tzinfo=pytz.utc)
    gotten = list(
        n_most_recent(
            now, mock_fetcher, num_items=10, days_back=4, later_than=later_than
        )
    )
    assert all([g['create_date'] > later_than.isoformat() for g in gotten])
    assert 2 == len(mock_fetcher.call_args_list)


def test_truncates_hours_et_al():
    now = datetime.datetime(
        year=1968, month=5, day=17, hour=2, minute=9, second=12, microsecond=3456
    )
    fetcher = mock.Mock()
    fetcher.return_value = []
    list(n_most_recent(now, fetcher, num_items=1, days_back=1))
    fetcher.assert_called_once_with(
        datetime.date(year=1968, month=5, day=17), later_than=None
    )


def test_doesnt_run_forever(db):
    mock_fetcher = mock.Mock()
    mock_fetcher.side_effect = lambda dt, later_than=None: fetch_day(
        db, dt, later_than=later_than
    )
    gotten = list(n_most_recent(now, mock_fetcher, num_items=10, days_back=2))
    assert len(gotten) == 8
    assert len(mock_fetcher.call_args_list) == 2


def test_doesnt_return_too_many_items(db):
    gotten = list(n_most_recent(now, partial(fetch_day, db), num_items=10, days_back=4))
    assert len(gotten) == 10
