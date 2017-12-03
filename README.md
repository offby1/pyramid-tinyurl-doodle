Following along http://chalice.readthedocs.io/en/latest/quickstart.html

First do

    $ python3 -m venv venv
    $ ./venv/bin/pip install -r dev-requirements.txt 

I've been using these commands to test stuff:

    $ ./venv/bin/pip install -r requirements.txt
    $ git submodule update
    $ ./venv/bin/chalice local

I suspect the above command does not automatically reload any of the python files after I hack on them, but otoh I don't need to reload after hacking on the template, since each request reloads the template.

    $ ./venv/bin/chalice deploy && ./venv/bin/http --pretty=format get https://v4ycr4gc52.execute-api.us-west-1.amazonaws.com/api/
