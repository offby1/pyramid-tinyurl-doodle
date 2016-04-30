#!/usr/bin/env python3

import io
import json
import logging
import subprocess

from tinyurl.module.dynamo import DynamoDB


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


logging.basicConfig(level=logging.INFO)

child = subprocess.Popen([
    'docker', 'run',
    '--link', 'db:db',
    'library/postgres',
    'psql',
    '-h', 'db',
    '-U', 'postgres',
    '-c', 'select row_to_json(hashes) from hashes order by create_date',
], stdout=subprocess.PIPE)

all_the_output, _ = child.communicate()
i = io.StringIO(all_the_output.decode('utf-8'))

d = DynamoDB()
d.batch_add_key_value_pairs(dicts_from_file(i))
