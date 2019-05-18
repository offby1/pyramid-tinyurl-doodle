import collections
import operator

from tinyurl.db import hashes


class DummyDatabase:
    def __init__(self):
        self.stuff = {}

        # For testing
        self.save_metrics = collections.Counter()

    def _save(self, key, value):
        self.stuff[key] = value
        self.save_metrics[key] += 1

    def add_if_not_present(self, key, value):
        if key not in self.stuff:
            self._save(key, value)

    def lookup(self, input):
        return self.stuff[input]

    def get_all(self):
        return sorted(self.stuff, key=operator.itemgetter('create_date'))


def test_different_inputs_different_outputs():
    inputs = ('http://whatever', 'doesnt actually have to be a URL actually')
    outputs = set()
    database = DummyDatabase()

    for input in inputs:
        outputs.add(hashes.long_url_to_short_string(input, database))

    assert len(outputs) == len(inputs)
    assert [len(o) for o in outputs] == [10, 10]


def test_round_trip():
    inputs = ('http://whatever', 'there are more things in your philosophy')
    database = DummyDatabase()

    for i in inputs:
        output = hashes.long_url_to_short_string(i, database)

        assert hashes.lengthen_short_string(output, database) == i


def test_same_URL_saves_at_most_once():
    database = DummyDatabase()

    long_url = 'a long, long, time ago'
    key1 = hashes.long_url_to_short_string(long_url, database)
    key2 = hashes.long_url_to_short_string(long_url, database)

    assert key1 == key2
    assert database.save_metrics[key1] == 1
