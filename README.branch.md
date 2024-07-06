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

Here's how the existing pyramid thing works:

```
144.217.82.212   200 GET    /shorten-/?input_url=https%3A%2F%2Fyt3.googleusercontent.com%2Fg9-WRx3NlxcsAFOHj8-ZJM8Nhjqd9UhTYDsolvup9j3-B2cNfXZg7Shd2C9TkX16zZKWZRyUP14%3Ds900-c-k-c0x00ffffff-no-rj
174.21.219.20    200 GET    /shorten-/?input_url=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dtell%2Byour%2Bcat%2Bi%2Bsaid%2Bpspspsps%26sca_esv%3D13f83d3e4d744b27%26sca_upv%3D1%26source%3Dhp%26biw%3D1440%26bih%3D790%26ei%3DT5lrZr7_Luy00PEPisOwkAU%26iflsig%3DAL9hbdgAAAAAZmunX9dwIaqSHINu3iv6arajh6H6yMUH%26oq%3Dtell%2Byour%2Bcat%2B%26gs_lp%3DEgNpbWciDnRlbGwgeW91ciBjYXQgKgIIADIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIzBdQAFiQC3AAeACQAQCYAS6gAYYEqgECMTS4AQHIAQD4AQGKAgtnd3Mtd2l6LWltZ5gCDqACxwTCAggQABiABBixA8ICCxAAGIAEGLEDGIMBwgIEEAAYA5gDAJIHAjE0oAetSg%26sclient%3Dimg%26udm%3D2&g-recaptcha-response=03AFcWeA5U_MlvMJAuxPb4jP34aRiX-9TaoxUlAbGTuBNz0LsK5nlw2ceNQrhEwuU_TqXdIzPD3aLV92kZlLx6XaQRh-laufm2rEeWDB__-Yd_ax0bTr1fud3DYTEuaFT33kjlwFQUDeeWOk8bpMwnKVmy3TE8lEpE5DEswIMkwFtTcbJ3HSjLP2zIYPIoJQjqslVKX1iTlolmI6hmnT8GvgM5I7BhVgfdJjAxM4hxZdiUiOCa44nAF10ShhwJh07-m7T-zApwRe-Fiqb8IysBwM8O3h7QRAKV2Fnx3fl5QfAgqaEve7RFc33etcvurtPM0Jbz0x-brp-fOkIB9KyRUDrZjHtepvQzTYfEREAdvao4Hw7oa0fmnKD2Et4GL6sI9D2jCWG_n2SHNWK_OLnOskpt9qcrsqcy73u6o-xfYuHyyiewk5ETy_bf1KQ1cpEeez1S64zXMv0Lh8KayGu6ZRKwxkc4wUcW5JD7HQy8z7zqCtAB1EUmnJDQ6DJ_ss8a7TUCClEuj_U9ZiaEiAwmac-bPDeeenPtV7XFSmjAdcLcwjvf6ew2_MT0JsQ3nQQIfQ_r18PY7JcQYrNn9Pa5sd9kG2-CiHcc0fcVl1jPpdtsX9oPX8Q0nBejEVstptuEewN9RVRagANGb5yNFLyRKPf6eC5Jx8TKCn0Hf_nyPOEweJCzJT92W4I
```

The second entry there came from the web UI (I can tell because it includes the "recaptcha" thingy, and because the IP address isn't `'144.217.82.212',  # solaria.tethera.net, rudybot's new home.`)

I guess, in django-y terms, the routing looks like

    path("shorten-/", app.views.shorten, name="shorten"),
    path("<short>", app.views.lengthen, name="lengthen"),
