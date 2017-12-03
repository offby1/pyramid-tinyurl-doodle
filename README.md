Following along http://chalice.readthedocs.io/en/latest/quickstart.html

First do

    $ ./venv/bin/pip install -r dev-requirements.txt 

Be sure to do `pip install chalice`, because:

- this code is but one branch of a project
- this code, as well as the other branches, probably have a `venv` directory
- the different branches probably want different versions of stuff in that venv directory (in particular, boto3)
- chalice will break if the venv has the wrong version of something
- `pip install chalice` will fix that breakage

I've been using these commands to test stuff:

    $ ./venv/bin/pip install -r requirements.txt
    $ ./venv/bin/chalice local

I suspect the above command does not automatically reload any of the python files after I hack on them, but otoh I don't need to reload after hacking on the template, since each request reloads the template.

    $ ./venv/bin/chalice deploy && ./venv/bin/http --pretty=format get https://v4ycr4gc52.execute-api.us-west-1.amazonaws.com/api/
