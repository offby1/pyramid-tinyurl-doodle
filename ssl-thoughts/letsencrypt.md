A while ago I tried letsencrypt, specifically "certbot", and found it overwhelmingly complex (despite the web page's describing it as simple).

Apparently there are other ways of getting a cert from letsencrypt; [this one](https://github.com/kshcherban/acme-nginx) is designed for nginx so might be usable.

Another option: lightsail.  Here's what I've done so far:

- created a lightsail instance that includes nginx out of the box.  It's at nginx.teensy.info
- started reading https://docs.bitnami.com/aws/how-to/generate-install-lets-encrypt-ssl/#alternative-approach

Sumbitch: https://nginx.teensy.info/ works and doesn't whine about invalid cert or anything.

Now I guess I gotta automatically renew the thing every few months, and the rejigger nginx to point to my app.

So the takeaway is: https://go-acme.github.io/lego/ is genuinely easy to use.

    sudo lego --tls --email="eric.hanchrow@gmail.com" --domains="teensy.info" --path="/etc/lego" run

did what it's sposed to.

Not quite there yet, though: chrome reports the page is "not fully secure" because

    This page is not secure.
    Resources - non-secure form
    This page includes a form with a non-secure "action" attribute.

That wasn't too hard to fix; I need to use "https://" in the action URL; I managed to get nginx to forward the scheme, and pyramid to honor it.

The one remaining problem: all the IP addresses in the logs are now 127.0.0.1

In particular:

  python3 -m pipenv run prequest --header Accept:text/json --header X-Real-IP:1.2.3.4 development.ini /wat > /dev/null
...
  2019-04-01T16:44:10.081Z INFO  [request_id][MainThread] 7f87c89d-325e-4313-bb33-fa7def6cda55 127.0.0.1 404 GET    /wat
