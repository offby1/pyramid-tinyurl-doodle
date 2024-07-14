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
    local flavor=${1:-dev}      # "dev" or "prod"

    ln --symbolic --verbose --force $(pwd)/git/post-checkout .git/hooks
    git checkout                # this causes the post-checkout hook to run

    # Use a python with sqlite support :-(
    # This is needed on my ec2 box
    if [ -x ~/.pyenv/versions/3.12.0a3/bin/python ]
    then
        poetry env use ~/.pyenv/versions/3.12.0a3/bin/python
    fi

    poetry install

    export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-project.${flavor}_settings}

    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    poetry run pytest
    DJANGO_SUPERUSER_PASSWORD=admin poetry run python3 manage.py createsuperuser --no-input --username=$USER --email=eric.hanchrow@gmail.com || true # "|| true" lets us get past "That username is already taken"

    case ${flavor} in
        dev)
            poetry run python manage.py runserver 0.0.0.0:8000
            ;;
        prod)
            poetry run python manage.py collectstatic
            DJANGO_SECRET=$(python3  -c 'import secrets; print(secrets.token_urlsafe(100))') docker-compose up --build
            ;;
        *)
            echo Dunno how to interpret flavor ${flavor}
    esac

}

main "$@"
