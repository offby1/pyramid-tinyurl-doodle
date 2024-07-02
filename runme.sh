#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./runme.sh

Sets up most things for you and starts the web server.

'
    exit
fi

cd "$(dirname "$0")"

main() {
    poetry install

    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    poetry run python manage.py runserver
}

main "$@"
