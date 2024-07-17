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

    # This is needed on my ec2 box ("20.04.6 LTS (Focal Fossa)").  I used to think it was because the python that came
    # preinstalled (3.8.10) didn't have sqlite support, but it does.  On the other hand, python3.8 simply seems too old
    # for the various packages on which this project depends, so we might as well use a new one.
    if [ -x ~/.pyenv/versions/3.12.0a3/bin/python ]
    then
        poetry env use ~/.pyenv/versions/3.12.0a3/bin/python

    # ... *sigh* and this is for MacOS.  It's first on my PATH, but other branches of this repo require that we "poetry
    # env use" an older version of python
    elif [ -x /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 ]
    then
        poetry env use /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
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
            poetry run python manage.py collectstatic --no-input
            poetry run gunicorn                                                                                         \
                   --access-logfile=-                                                                                   \
                   --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'    \
                   --capture-output                                                                                     \
                   --log-level=DEBUG                                                                                    \
                   project.wsgi
            ;;
        *)
            echo Dunno how to interpret flavor ${flavor}
    esac

}

main "$@"
