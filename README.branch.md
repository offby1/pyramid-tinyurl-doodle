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

* [ ] Go through [the nginx beginner's guide](http://nginx.org/en/docs/beginners_guide.html) slowly and carefully
* [ ] plop it on an actual EC2 box and test it in "production" mode.
  In particular: the recaptcha
* [ ] Again look into replacing `runme.sh` with ["just"](https://just.systems/man/en/)

## DONE

* [x] figure out how to deal with secrets

  <https://docs.docker.com/engine/swarm/secrets/#build-support-for-docker-secrets-into-your-images> suggests it's straightforward—and in fact I've done something similar in the `docker-take-three` branch.  It's confusing, though, since much of the documentation around docker secrets refers to "docker swarm", which is ... I dunno? An alternative to docker-compose?
