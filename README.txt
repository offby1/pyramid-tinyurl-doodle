tinyurl README
==================

Getting Started Locally
-----------------------

- cd <directory containing this file>

- cp git/post-checkout .git/hooks

- $VENV/bin/pip install -r dev-requirements.txt

- $VENV/bin/pip install -r requirements.txt

Note that the various "*requirements.txt" files, despite being checked
in to git, are automatically generated from the corresponding
"*requirements.in" files.  See https://github.com/nvie/pip-tools for
details.  Also note that, to regenerate those files (at least, on my
Mac, using Python 3), you gotta put LC_ALL=en_US.utf-8 in the
environment, like this:

    $ LC_ALL=en_US.utf-8 pip-compile dev-requirements.in > dev-requirements.txt

lest ye get an annoying exception:

    RuntimeError: Click will abort further execution because Python 3
    was configured to use ASCII as encoding for the
    environment. Either switch to Python 2 or consult
    http://click.pocoo.org/python3/ for mitigation steps.

- $VENV/bin/python setup.py develop

- $VENV/bin/py.test tinyurl

- $VENV/bin/initialize_tinyurl_db development.ini

- $VENV/bin/pserve --reload development.ini


Doing The Docker Thang
----------------------

In production:

$ docker run --detach  --name tinyurl -p 80:80  offby1/tinyurl

Upgrading:

Use the desktop (below) to build a new docker image, and push it.

$ docker build .
$ docker images  # note the ID of the image you just built
$ docker tag -f deadbeef offby1/tinyurl
$ docker push offby1/tinyurl # this is annoyingly slow

Then, on the production server:

$ docker pull offby1/tinyurl
$ docker rm -f tinyurl && docker run --detach --link db:db --name tinyurl -p 80:80  offby1/tinyurl

On the desktop:

$ vagrant up
