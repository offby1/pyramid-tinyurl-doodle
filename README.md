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
to find them (tl;dr: mine are in `~/.aws/credentials`).  Then ---
assuming you've got
a [virtualenv](https://virtualenv.pypa.io/en/latest/) somewhere, and
stored its location in the variable `VENV` --- do:

    $ cd <directory containing this file>
    $ cp git/post-checkout .git/hooks
    $ $VENV/bin/pip install -r dev-requirements.txt
    $ $VENV/bin/pip install -r requirements.txt

> Note that the various `*requirements.txt` files, despite being
> checked in to git, are automatically generated from the
> corresponding `*requirements.in` files.  See
> [the pip-tools docs](https://github.com/nvie/pip-tools) for details.

    $ $VENV/bin/python setup.py develop
    $ $VENV/bin/py.test tinyurl
    $ $VENV/bin/pserve --reload development.ini
