Rewrote it in Django.

Uses sqlite instead of dynamodb:

* django doesn't work well with dynamodb (or any nosql database);
* sqlite otta be fine given how little data we have

    As of 2024-07-01T08:09:41-0700:

    ```
    Item count
    10,689
    Table size
    2.2 megabytes
    Average item size
    204.17 bytes
    ```

  We could back up sqlite by pushing it to dynamodb.  We could easily teach the existing `sync-ddb-data` management command to do that.

  (Have "cron" or "systemd" or whatever run it every now and then)

  Even easier: run `python manage.py dumpdata`, and send that to an S3 bucket.

TODO:

- [ ] plop it on an actual EC2 box and test it in "production" mode.
  In particular: the recaptcha
