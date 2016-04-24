import uuid

import database
import dynamo


import pytest


def test_it_really_is_abstract ():
    class MissingRequiredMethods(database.DatabaseMeta):
        pass

    with pytest.raises(TypeError):
        MissingRequiredMethods()


def test_dynamo_works():
    d = dynamo.DynamoDB()

    random_value = str(uuid.uuid4())

    d.save('key', random_value)
    assert(d.lookup('key') == random_value)
