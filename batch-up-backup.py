#!/usr/bin/env python3

import io
import json
import pprint

def dicts_from_file(inf):
    """Read output from a poor man's postgresql export: "select
    row_to_json(x) from x".  The output isn't JSON, exactly; instead,
    most (but not all) lines are themselves JSON objects.  We read
    each such line, ignoring the others, and yield the resulting dict.

    """
    for line in inf:
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

pprint.pprint(list(batches(10, open('semi-json-db-dump'))))
# Someday I expect I'll do something like ...
import subprocess
child = subprocess.Popen([
    'docker', 'run',
    '--link', 'db:db',
    'library/postgres',
    'psql',
    '-h', 'db',
    '-U', 'postgres',
    '-c', 'select row_to_json(hashes) from hashes',
], stdout=subprocess.PIPE)

all_the_output, _ = child.communicate()
pprint.pprint(list(batches(10, io.StringIO(child.stdout))))
