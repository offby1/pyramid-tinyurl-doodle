set quiet := true
set unstable

# The `tput` mumbo-jumbo just colors the text green; see https://stackoverflow.com/a/20983251

flavor := "dev"
export DJANGO_SETTINGS_MODULE := env("DJANGO_SETTINGS_MODULE", "project." + flavor + "_settings")

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

[group('django')]
[private]
django-prep: all-but-django-prep makemigrations migrate
    if ! DJANGO_SUPERUSER_PASSWORD=admin poetry run python3 deckgen2/manage.py createsuperuser --no-input --username=$USER --email=eric.hanchrow@gmail.com;  then echo "$(tput setaf 2)'That username is already taken' is OK! ctfo$(tput sgr0)"; fi

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
sync: django-prep (manage "sync-ddb-data")

# Do all preparations, then run.  `just flavor=prod runme` for production.
[group('teensy')]
[script('sh')]
runme *options: git-prep django-prep test
    set -eu

    if [ "{{ flavor }}" = "prod" ]
    then
       poetry run python manage.py collectstatic --no-input
       poetry run gunicorn                                                                                      \
              --access-logfile=-                                                                                \
              --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
              --logger-class project.wsgi.TolerableLogger                                                       \
              project.wsgi

    else
       poetry run python manage.py runserver 0.0.0.0:8000
    fi

[group('teensy')]
test *options: django-prep
    poetry run pytest --exitfirst --create-db {{ options }}

#  Nix the virtualenv and anything not checked in to git.
clean:
    poetry env info --path | xargs --no-run-if-empty rm -rf
    git clean -dx --interactive --exclude='*.sqlite3'

[group('prod')]
monitor:
    tmux new-window -n "nginx"   "setterm -linewrap off; tail --follow=name --retry /var/log/nginx/{access,error}.log"
    tmux new-window -n "pyramid" "setterm -linewrap off; journalctl --unit=teensy.service --follow --output=cat"
