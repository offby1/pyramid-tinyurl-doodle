Getting Started Locally
-----------------------

To generate the cookie secret (on OS X use `gtr` instead of `tr`; get it from `brew install coreutils`):

    $ cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

To generate the recaptcha secret:

Surprise!  It's already generated.  Just go to
https://www.google.com/recaptcha/admin#site/320420908, log in as me,
scrape the "Secret Key" out of the "Keys" section, then save it into
`.recaptcha_secret`.

Ensure you've got Amazon AWS config and credentials,
wherever
[boto](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration) expects
to find them (tl;dr: mine are in `~/.aws/credentials`).  Then do:

    $ brew install pipenv # or pip install pipenv
    $ cd <directory containing this file>
    $ cp git/post-checkout .git/hooks
    $ pipenv install --dev
    $ pipenv run python3 setup.py develop
    $ pipenv run python3 -m pytest tinyurl

    $ pipenv run pserve --reload development.ini
or
    $ sudo yum install nginx
    $ sudo cp nginx-default.conf /etc/nginx/nginx.conf # for Amazon Linux anyway
    $ sudo /etc/init.d/nginx start
    $ pipenv run pserve production.ini
