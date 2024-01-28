#!/bin/sh

here="$(cd "$(dirname "$0")" && pwd)"
set -x

cd "${here}"

poetry install

set -e
poetry run pytest tinyurl/tests
poetry run prequest -d development.ini /sw97SVacIe
poetry run pserve development.ini
