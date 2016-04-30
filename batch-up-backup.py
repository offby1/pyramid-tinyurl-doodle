#!/usr/bin/env python3

import json
import pprint

def rows():
    """Read output from a poor man's postgresql export: "select
    row_to_json(x) from x".  The output isn't JSON, exactly; instead,
    most (but not all) lines are themselves JSON objects.  We read
    each such line, ignoring the others, and yield the resulting dict.

    """
    with open('semi-json-db-dump') as inf:
        for index, line in enumerate(inf):
            if not line.startswith(' {'):
                continue
            yield json.loads(line)


# How many times have I written this ...
def batches(batchsize, items):
    current_batch = []
    for item in items:
        if len(current_batch) == batchsize:
            yield current_batch
            current_batch = []
        current_batch.append(item)

    if current_batch:
        yield current_batch

pprint.pprint(list(batches(10, rows())))
