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

  We will back up sqlite by having "cron" or "systemd" or whatever run `python manage.py sync-ddb-data` every now and then.

  I have another management command, `backup-db-to-s3`, that isn't needed any more, but I feel like keeping it around for some reason.

TODO:

- [ ] plop it on an actual EC2 box and test it in "production" mode.
  In particular: the recaptcha
