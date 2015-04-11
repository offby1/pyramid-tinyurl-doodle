tinyurl README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -r requirements.txt

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_tinyurl_db development.ini

- $VENV/bin/pserve development.ini

Note that 'run', 'runapp.py', and 'Procfile' are for heroku.

The only way I found to get it working on OS X was to install http://postgresapp.com/.
To run it on OS X:

        pserve --reload development.ini 
