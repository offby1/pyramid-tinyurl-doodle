Might's well rewrite it in Django, eh what?

While we're at it, let's use sqlite instead of dynamodb:

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

    However if we use sqlite we'll want some way to back it up -- [`VACUUM INTO`](https://www.sqlite.org/lang_vacuum.html#vacuuminto) seems to be it.

  I imagine a little python script that will
      * rename any existing backup
      * make a new backup
      * delete the older backup
  and just have "cron" or "systemd" or whatever run it every coupla hours.
  Ideally we'd then copy the backup someplace off of the box, maybe just my laptop, or a different EC2 instance if I have one laying around.
