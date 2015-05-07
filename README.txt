tinyurl README
==================

Getting Started Locally
-----------------------

- cd <directory containing this file>

- cp git/post-checkout .git/hooks

- $VENV/bin/pip install -r requirements.txt

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_tinyurl_db development.ini

- $VENV/bin/pserve --reload development.ini

Note that 'run', 'runapp.py', and 'Procfile' are for heroku.

The only way I found to get it working on OS X was to install
http://postgresapp.com/ -- I'd tried "brew install postgresql", as
well as installing from
http://www.enterprisedb.com/products-services-training/pgdownload#osx;
but in both cases, I couldn't figure out how to set up postgres' users
:-(  Somehow postgresapp Just Works™.

Doing The Heroku Thing
----------------------

Can't remember :-|


Doing The Docker Thang
----------------------

$ vagrant up
