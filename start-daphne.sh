#!/usr/bin/env bash

# From https://sharats.me/posts/shell-script-best-practices/

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

cd "$(dirname "$0")"

main() {
    ./.venv/bin/python3 manage.py makemigrations
    ./.venv/bin/python3 manage.py migrate
    ./.venv/bin/python3 manage.py collectstatic --no-input

    /django-project/.venv/bin/daphne                                                            \
        --verbosity                                                                             \
        3                                                                                       \
        --bind                                                                                  \
        0.0.0.0                                                                                 \
        --port                                                                                  \
        8000                                                                                    \
        --log-fmt="%(asctime)sZ %(levelname)s %(name)s %(filename)s %(funcName)s %(message)s"   \
        project.asgi:application

}

main "$@"
