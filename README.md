# Getting Started Locally

## Cookie secret

To generate the cookie secret (on OS X use `gtr` instead of `tr`; get it from `brew install coreutils`):

    $ cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

## Recaptcha secret

To generate the recaptcha secret:

Surprise!  It's already generated.  Just go to
[google](https://www.google.com/recaptcha/admin#site/320420908), log
in as me, scrape the "Secret Key" out of the "Keys" section, then save
it into `.recaptcha_secret`.

## Git version info thingy

    $ cp git/post-checkout .git/hooks

## AWS credentials

Ensure you've got Amazon AWS config and credentials, wherever
[boto](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration)
expects to find them (tl;dr: mine are in `~/.aws/config` and
`~/.aws/credentials`).  Then do:

    $ cd <directory containing this file>

## MacOS with homebrew

    $ brew install python3 pipenv
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install
    $ python3 -m pipenv run python3 setup.py develop
    $ python3 -m pipenv run pserve development.ini

## CentOS6

    $ sudo yum install -y epel-release
    $ sudo yum install -y python34
    $ python3 -m ensurepip --user
    $ python3 -m pip install --user pipenv
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install
    $ python3 -m pipenv run python setup.py develop
    $ python3 -m pipenv run pserve development.ini

## CentOS7

    $ sudo yum install -y epel-release
    $ sudo yum install -y python36
    $ python36 -m ensurepip --user
    $ python36 -m pip install --user pipenv
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python36 -m pipenv install
    $ python36 -m pipenv run python setup.py develop
    $ python36 -m pipenv run pserve development.ini

## Debian-like

Tested on:

- Debian 9.4.0 "Stretch"
- Ubuntu 14.04 "Trusty"
- Ubuntu 16.04 "Xenial"
- Ubuntu 18.04 "Bionic"

Steps:

    $ sudo apt-get update # oddly necessary on Ubuntu 16+
    $ sudo apt-get install python3-pip
    $ python3 -m pip install --user pipenv # scary but harmless syntax errors on trusty
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install
    $ python3 -m pipenv run python setup.py develop
    $ python3 -m pipenv run pserve development.ini

## Amazon Linux release 2017.03

(or, at least, [a vagrant box that purports to resemble
it](https://app.vagrantup.com/mvbcoding/boxes/awslinux))

    $ sudo yum install git python35 python35-pip
    $ python3 -m pip install --user --upgrade pip
    $ python3 -m pip install --user pipenv
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install
    $ python3 -m pipenv run python setup.py develop
    $ python3 -m pipenv run pserve development.ini

## Amazon Linux release 2018.03

Not sure how I got python3; I suspect it just comes with Amazon Linux.

    $ python3 -m pip install --user --upgrade pip # probably not necessary but what the hell
    $ python3 -m pip install --user pipenv
    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install
    $ python3 -m pipenv run python setup.py develop
    $ python3 -m pipenv run pserve development.ini

# Testing

Run tests like this:

    $ export PIPENV_VENV_IN_PROJECT=1
    $ python3 -m pipenv install --dev
    $ python3 -m pipenv run python3 setup.py develop
    $ python3 -m pipenv run py.test -s $(python3 -m pipenv --where)/tinyurl/tests/

You can also run a random URL through it without having to start the server:

    $ python3 -m pipenv run prequest development.ini  /sw97SVacIe

# Normalize formatting with "black"

    $ PIPENV_VENV_IN_PROJECT=1 python3 -m pipenv run black tinyurl/
