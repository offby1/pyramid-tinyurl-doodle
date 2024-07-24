set quiet := true
set unstable

# The `tput` mumbo-jumbo just colors the text green; see https://stackoverflow.com/a/20983251

flavor := "dev"
export AWS_DEFAULT_REGION := "us-west-1"
export DJANGO_SETTINGS_MODULE := env("DJANGO_SETTINGS_MODULE", "project." + flavor + "_settings")
export POETRY_VIRTUALENVS_IN_PROJECT := "false"

[private]
default:
    just --list

# Set up the post-checkout hook so that the server knows its git commit hash.
[group('git')]
git-prep:
    ln --symbolic --verbose --force  {{justfile_directory()}}/git/post-checkout .git/hooks
    git checkout

# install into the virtualenv a recent python (if we can find one)
[group('virtualenv')]
[macos]
poetry-env-prep:
    p=/Library/Frameworks/Python.framework/Versions/3.12/bin/python3; if [ -x $p ] ; then poetry env use $p ; fi

# install into the virtualenv a recent python (if we can find one)
[group('virtualenv')]
[linux]
poetry-env-prep:
    p=$HOME/.pyenv/versions/3.12.0a3/bin/python; if [ -x $p ] ; then poetry env use $p ; fi

[group('virtualenv')]
poetry-install: poetry-env-prep
    poetry install

[group('django')]
[private]
all-but-django-prep: poetry-env-prep poetry-install git-prep

# To prevent the password from being hard-coded in this file, be sure to invoke this like
# `DJANGO_SUPERUSER_PASSWORD=SEKRIT just django-superuser`
# `just manage changepassword` if you forget it.
[group('django')]
[private]
django-superuser: all-but-django-prep makemigrations migrate
    if ! poetry run python3 manage.py createsuperuser --no-input --username=$USER --email=eric.hanchrow@gmail.com;  then echo "$(tput setaf 2)'That username is already taken' is OK! ctfo$(tput sgr0)"; fi

[group('django')]
[private]
manage *options: all-but-django-prep
    poetry run python manage.py {{ options }}

[group('django')]
makemigrations *options: (manage "makemigrations " + options)

[group('django')]
migrate *options: makemigrations (manage "migrate " + options)

# Ensure that our local db holds a complete copy of dynamodb, and vice-versa
[group('teensy')]
sync: django-superuser (manage "sync-ddb-data")

[private]
collectstatic: all-but-django-prep
    poetry run python manage.py collectstatic --no-input

# Do all preparations, then run.  `just flavor=prod runme` for production.
[group('teensy')]
[script('sh')]
runme *options: git-prep django-superuser test collectstatic
    set -eu

    if [ "{{ flavor }}" = "prod" ]
    then
       poetry run gunicorn                                                                                      \
              --access-logfile=-                                                                                \
              --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
              --logger-class project.wsgi.TolerableLogger                                                       \
              project.wsgi

    else
       poetry run python manage.py runserver 0.0.0.0:8000
    fi

[group('teensy')]
test *options: django-superuser
    poetry run pytest --exitfirst --failed-first --create-db {{ options }}

#  Nix the virtualenv and anything not checked in to git.
clean:
    poetry env info --path | xargs --no-run-if-empty rm -rf
    git clean -dx --interactive --exclude='*.sqlite3'
    docker rm -f teensy-django-1
    docker rm -f  teensy-nginx-1
    docker rmi -f teensy-django

# See "systemctl status nginx.service" and "journalctl -xeu nginx.service" for details about nginx
[group('prod')]
monitor:
    tmux new-window -n "nginx"   "setterm -linewrap off; tail --follow=name --retry /var/log/nginx/{access,error}.log"
    tmux new-window htop

[group('docker')]
up *options: git-prep collectstatic
    # It'd be nice if I could use one of the `dotenv-` settings
    # https://just.systems/man/en/chapter_27.html#table-of-settings instead of this mysterious xargs thing, but those
    # settings are only available when this justfile is "load"ed, but config_directory() is only available inside a
    # recipe!
    # https://discord.com/channels/695580069837406228/695580069837406231/1265126046588600322
    export $(xargs < "{{ config_directory() }}/info.teensy.teensy-django/.env") ; docker compose up {{ options }}
