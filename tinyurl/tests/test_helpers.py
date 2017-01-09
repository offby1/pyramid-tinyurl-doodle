import datetime

import mock
from tinyurl import helpers

def make_fetcher(items_per_day):

    def stub_day_fetcher(dt):

        def random_string():
            import string
            return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        import random
        return [{
            'human_hash': random_string(),
            'create_date': (dt + datetime.timedelta(seconds=random.random() * 24 * 3600)).isoformat ()
        } for i in range(items_per_day)]

    return stub_day_fetcher

now = datetime.datetime(year=1968, month=5, day=17)

def test_n_most_recent():
    gotten = list(helpers.n_most_recent (now, make_fetcher(4), num_items=10, days_back=4))
    assert len(gotten) == 10


def test_truncates_hours_et_al():
    now = datetime.datetime(year=1968, month=5, day=17, hour=2, minute=9, second=12, microsecond=3456)
    fetcher = mock.Mock()
    fetcher.return_value = []
    list(helpers.n_most_recent (now, fetcher, num_items=1, days_back=1))
    fetcher.assert_called_once_with(datetime.date(year=1968, month=5, day=17))


def test_doesnt_run_forever():
    gotten = list(helpers.n_most_recent (now, make_fetcher(1), num_items=10, days_back=4))
    assert len(gotten) == 4


def test_return_too_many_items():
    gotten = list(helpers.n_most_recent (now, make_fetcher(1000), num_items=10, days_back=4))
    assert len(gotten) == 10
