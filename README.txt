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

To back up a running docker DB:

    $ docker run    --link db:db library/postgres pg_dump -h db -U postgres -t hashes > hashes.sql

To load that into another DB:

    $ docker run -i --link db:db library/postgres psql -a -h db -U postgres  < /vagrant/hashes.sql

... although you might need to delete the existing "hashes" table first.

To get a SQL prompt:

    $ docker run -it --link db:db library/postgres psql -h db -U postgres

To nix a spammy entry from the above SQL prompt:

    postgres=# delete  from hashes where human_hash = 'rgufGVicnL';
    DELETE 1
    postgres=#
