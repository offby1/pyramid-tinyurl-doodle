import hashes


def test_different_inputs_different_outputs():
    inputs = ('http://whatever', 'doesnt actually have to be a URL actually')
    outputs = set()
    for input in inputs:
        outputs.add(hashes.long_url_to_short_string(input))

    assert len(outputs) == len(inputs)
    assert [len(o) for o in outputs] == [6, 6]


def test_round_trip():
    input = 'http://whatever'
    output = hashes.long_url_to_short_string(input)

    assert(hashes.lengthen_short_string(output) == input)
