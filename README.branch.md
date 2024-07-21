# WASSUP HOMIES

Rewrote it in Django.

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

  We will back up sqlite by having "cron" or "systemd" or whatever run `python manage.py sync-ddb-data` every now and then.

  I have another management command, `backup-db-to-s3`, that isn't needed any more, but I feel like keeping it around for some reason.

## No, really; wassup

Despite all my recent hackage around Docker, I'm *really* trying to understand Nginx. I don't expect to use Docker in production; rather, it's a convenient way to run nginx locally while I figure out how to configure it.

I'm already using nginx in production, to do SSL termination (I know of no better way).

If I'm lucky and clever, I'll be able to run the master branch *and* this branch in production at the same time, with the same nginx instance, but with two different sets of config.  Ideally, I'd eventually decide this branch is awesome, and will just shut down the other branch and remove its config.

## TODO

* [ ] Test with rudybot!
  Pretty sure I need to whitelist its IP address.
  A recent log against the pyramid server looks like `144.217.82.212 - - [14/Jul/2024:19:09:16 +0000] "GET /shorten-/?input_url=https%3A%2F%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2Fmy.what.a.long.url%2Fyou%2Fhave%2Fgrandma%2F HTTP/1.1" 200 30 "-" "Racket/7.9 (net/http-client)"` fwiw
* [ ] Update the upstart, or systemd, or init.d, or whatever-the-hell-it-is, if needed.
* [ ] Update the nginx.conf again, to have just one server
* [ ] Set up cron job to run `sync-ddb-data`, as above.
   `DJANGO_SETTINGS_MODULE=project.prod_settings nice  ~/git-repos/me/teensy-django/.venv/bin/python manage.py sync-ddb-data` will probably do it.
* [ ] Again look into replacing `runme.sh` with ["just"](https://just.systems/man/en/)
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
* [x] Consider [whitenoise](https://whitenoise.readthedocs.io/en/latest/) instead of a special section for nginx
