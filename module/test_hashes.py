import hashes


class DummyDatabase:
    def __init__(self):
        self.stuff = {}

    def save(self, key, value):
        self.stuff[key] = value

    def lookup(self, input):
        return self.stuff[input]


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

        assert(hashes.lengthen_short_string(output, database) == i)
