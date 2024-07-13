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
    # Use a python with sqlite support :-(
    # This is needed on my ec2 box
    if [ -x ~/.pyenv/versions/3.12.0a3/bin/python ]
    then
        poetry env use ~/.pyenv/versions/3.12.0a3/bin/python
    fi

    poetry install

    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    poetry run pytest
    DJANGO_SUPERUSER_PASSWORD=admin poetry run python3 manage.py createsuperuser --no-input --username=$USER --email=eric.hanchrow@gmail.com || true # "|| true" lets us get past "That username is already taken"
    ln --symbolic --verbose --force $(pwd)/git/post-checkout .git/hooks
    git checkout
    #poetry run python manage.py runserver 0.0.0.0:8000
    poetry run python manage.py collectstatic --no-input
    # TODO -- run nginx to handle the static files.
    poetry run gunicorn project.wsgi
}

main "$@"
