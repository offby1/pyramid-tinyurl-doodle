# WASSUP HOMIES

## How to get it all going
### Run it locally

`just runme` # https://just.systems/

### prod

Set up a cloud machine as per <https://gitlab.com/offby1/bridge-server/-/blob/dcfc26bfa7bd5d28edd2edf0a2f4070c39ff900f/docs/README.ubuntu-hetz.setup.md>

Now run `just prod`.  This works for both the initial deployment, and for updates.

## TODO

* [ ] Set up cron job to run `sync-ddb-data`, as above.
   `DJANGO_SETTINGS_MODULE=project.prod_settings nice  ~/git-repos/me/teensy-django/.venv/bin/python manage.py sync-ddb-data` will probably do it.

   I might not need to do this: I run `sync-ddb-data` every time I deploy, which might be enough.

### Easy Auth

* [ ] <https://www.photondesigner.com/articles/email-sign-in>

## DONE

* [x] figure out how to deal with Docker secrets

  <https://docs.docker.com/engine/swarm/secrets/#build-support-for-docker-secrets-into-your-images> suggests it's straightforward—and in fact I've done something similar in the `docker-take-three` branch.  It's confusing, though, since much of the documentation around docker secrets refers to "docker swarm", which is ... I dunno? An alternative to docker-compose?
* [x] Go through [the nginx beginner's guide](http://nginx.org/en/docs/beginners_guide.html) slowly and carefully
  Not very informative, as it happens :-|
* [x] plop it on an actual EC2 box and test it in "production" mode.
  In particular: the recaptcha
* [x] Come up with a better django admin password, and a better mechanism for getting it onto the prod host
  The password is now in bitwarden and Firefox.  The "better mechanism" is just running `DJANGO_SETTINGS_MODULE=project.prod_settings poetry run python manage.py changepassword ubuntu` at the command line.
* [x] Tell Google not to index the site
* [x] Tweak gunicorn logging so it puts the actual IP address in the log, not `127.0.0.1`
* [x] Again look into replacing `runme.sh` with ["just"](https://just.systems/man/en/)
* [x] Consider [whitenoise](https://whitenoise.readthedocs.io/en/latest/) instead of a special section for nginx
* [x] Test with rudybot!
  Pretty sure I need to whitelist its IP address.
  A recent log against the pyramid server looks like `144.217.82.212 - - [14/Jul/2024:19:09:16 +0000] "GET /shorten-/?input_url=https%3A%2F%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2F HTTP/1.1" 200 30 "-" "Racket/7.9 (net/http-client)"` fwiw
* [x] Update the nginx.conf again, to have just one server
* [x] Figure out why my old "teensy-2022" host died :-|
  tl;dr: `StartLimitAction=reboot` 🤢
  All I remember:
  - I was fiddling the `teensy.service` file, and did something like `sudo systemctl start teensy` to start it
  - systemctl said something like "golly I noticed some config files have changed; please do `systemctl daemon-reload the world` or something
  - from that point on it was weirdly unresponsive -- CPU usage went to about 60%, and I couldn't ssh in
  - perhaps attach that old root disk to the new host, and poke around in the logs
* [x] Update the systemd file.
## Rewrite notes
Rewrote it in Django -- it used to use Pyramid.

Uses sqlite instead of dynamodb:

* django doesn't work well with dynamodb (or any nosql database);
* sqlite otta be fine given how little data we have

    As of 2024-07-01T08:09:41-0700:

    ```text
    Item count
    10,689
    Table size
    2.2 megabytes
    Average item size
    204.17 bytes
    ```

  We will back up sqlite by having "cron" or "systemd" or whatever run `python manage.py sync-ddb-data` every now and then.  Or, you know, I'll just run that when I think of it :-)

  I have another management command, `backup-db-to-s3`, that isn't needed any more, but I feel like keeping it around for some reason.
