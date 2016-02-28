To generate the cookie secret:

    $ cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

To generate the recaptcha secret:

Surprise!  It's already generated.  Just go to
https://www.google.com/recaptcha/admin#site/320420908, log in as me,
and scrape the "Secret Key" out of the "Keys" section.
