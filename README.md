# Getting Started Locally

## Cookie secret

To generate the cookie secret (on OS X use `gtr` instead of `tr`; get it from `brew install coreutils`):

    $ cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

## Recaptcha secret

To generate the recaptcha secret:

Surprise!  It's already generated.  Just go to [google](https://www.google.com/recaptcha/admin#site/320420908), log in
as me, click the gear, click the "reCAPTCHA keys" thing, click "copy secret key", then save it into `.recaptcha_secret`.

## Git version info thingy

    $ cp git/post-checkout .git/hooks

## AWS credentials

Ensure you've got Amazon AWS config and credentials, wherever
[boto](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration)
expects to find them (tl;dr: mine are in `~/.aws/config` and
`~/.aws/credentials`).  Then do:

    $ cd <directory containing this file>

## Running as a service
### Systemd

For systems that use "systemd" (like Ubuntu 20.05 "focal"), drop `teensy.service` into `/etc/systemd/system`.
Then do `sudo systemctl enable teensy.service`; to actually start it, do `sudo systemctl start teensy` and to stop it do `sudo systemctl stop teensy`.

Tail the logs via `journalctl -f  -u teensy | less +F --chop`.

### Upstart
For systems that use "upstart" (like Amazon Linux AMI release 2018.03), you can just drop `teensy.conf` into `/etc/init`.


## Building via poetry
Note: do `git clean -dxff`, with two `f`s, if you want to nuke the world.  That's because there's a git repo in `.venv` that won't go away without the second `f`, and the lingering presence of that mostly-empty `.venv` causes mysterious failures like

    $ python3 -m poetry build
    [OSError 2]: No such file or directory: python

This seems to suffice:

- `export POETRY_VIRTUALENVS_IN_PROJECT=true`
- `python3 -m poetry install`
- `python3 -m poetry run pytest`
- `python3 -m poetry run prequest development.ini /sw97SVacIe`
