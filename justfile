set quiet := true
set unstable

# The `tput` mumbo-jumbo just colors the text green; see https://stackoverflow.com/a/20983251

flavor := "dev"

DJANGO_SECRET_DIRECTORY := config_directory() / "info.teensy.teensy-django"

export AWS_DEFAULT_REGION := "us-west-1"
export DJANGO_SECRET_KEY_FILE := DJANGO_SECRET_DIRECTORY / "django_secret_key"
export DJANGO_SETTINGS_MODULE := env("DJANGO_SETTINGS_MODULE", "project." + flavor + "_settings")
export RECAPTCHA_SECRET_FILE := DJANGO_SECRET_DIRECTORY / "recaptcha_secret"

[private]
default:
    just --list

# Set up the post-checkout hook so that the server knows its git commit hash.
[group('git')]
git-prep:
    PATH=/opt/homebrew/opt/coreutils/libexec/gnubin/:$PATH ln --symbolic --force  {{justfile_directory()}}/git/post-checkout .git/hooks
    git checkout

[group('virtualenv')]
uv-install:
    uv sync

[group('django')]
[private]
all-but-django-prep: uv-install git-prep

# To prevent the password from being hard-coded in this file, be sure to invoke this like
# `DJANGO_SUPERUSER_PASSWORD=SEKRIT just django-superuser`
# `just manage changepassword` if you forget it.
[group('django')]
[private]
django-superuser: all-but-django-prep makemigrations migrate
    if ! uv run python3 manage.py createsuperuser --no-input --username=$USER --email=eric.hanchrow@gmail.com;  then echo "$(tput setaf 2)'That username is already taken' is OK! ctfo$(tput sgr0)"; fi

[group('django')]
[private]
manage *options: all-but-django-prep ensure-django-secret
    uv run python manage.py {{ options }}

[group('django')]
makemigrations *options: (manage "makemigrations " + options)

[group('django')]
migrate *options: makemigrations (manage "migrate " + options)

# Ensure that our local db holds a complete copy of dynamodb, and vice-versa
[group('teensy')]
sync: django-superuser (manage "sync-ddb-data")

[private]
collectstatic: all-but-django-prep (manage "collectstatic --no-input")

# Do all preparations, then run.  `just flavor=prod runme` for production.
[group('teensy')]
[script('sh')]
runme *options: git-prep django-superuser test collectstatic
    set -eu

    if [ "{{ flavor }}" = "prod" ]
    then
       uv run gunicorn                                                                                      \
              --access-logfile=-                                                                                \
              --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
              --logger-class project.wsgi.TolerableLogger                                                       \
              project.wsgi

    else
       uv run python manage.py runserver 0.0.0.0:8000
    fi

[group('teensy')]
test *options: django-superuser
    uv run pytest --exitfirst --failed-first --create-db {{ options }}

#  Nix the virtualenv and most stuff not checked in to git, but leave the database.
clean:
    git clean -dx --interactive --exclude='*.sqlite3'
    -docker compose down --volumes

nuke: clean
    -rm -v *.sqlite3

[private]
django-secret-directory:
    mkdir -vp "{{ DJANGO_SECRET_DIRECTORY }}"

[private]
[script('bash')]
ensure-django-secret: django-secret-directory
    set -euo pipefail
    PATH=/opt/homebrew/opt/coreutils/libexec/gnubin/:$PATH
    touch "{{ DJANGO_SECRET_KEY_FILE }}"
    if [ ! -f "{{ DJANGO_SECRET_KEY_FILE }}" -o $(stat --format=%s "{{ DJANGO_SECRET_KEY_FILE }}") -lt 50 ]
    then
    python3  -c 'import secrets; print(secrets.token_urlsafe(100))' > "{{ DJANGO_SECRET_KEY_FILE }}"
    fi

[group('docker')]
[script('bash')]
up *options: git-prep collectstatic
    set -euo pipefail

    export AWS_ACCESS_KEY_ID=$(uv run python parse-aws-config.py aws_access_key_id)
    export AWS_SECRET_ACCESS_KEY=$(uv run python parse-aws-config.py aws_secret_access_key)
    export DJANGO_SECRET_KEY=$(cat "${DJANGO_SECRET_KEY_FILE}")
    export RECAPTCHA_SECRET=$(cat "${RECAPTCHA_SECRET_FILE}")
    docker compose up --build {{ options }}

[group('docker')]
[script('bash')]
prod *options:
    set -euo pipefail

    export CADDY_HOSTNAME=teensy.info
    export COMPOSE_PROFILES=prod
    export DJANGO_SETTINGS_MODULE=project.prod_settings
    export DOCKER_CONTEXT=teensy-prod

    just up {{ options }} --detach
    docker compose logs django --follow
