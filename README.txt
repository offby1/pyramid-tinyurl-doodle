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

To nix all spammy entries (on the assumption that the only legitimate entries came from rudybot and hence have long_urls that are longer than about 70 characters):

...
     2015-09-20 03:55:59.946079+00 | kFuaIBY6fE | http://vtvcab360.com/internet-vtvcab/
     2015-09-23 11:59:54.012979+00 | AL2N7idPXs | http://www.sunfrogshirts.com/X839?9983
     2015-09-23 19:22:40.870728+00 | dboPyzhFiw | http://www.musicaccesorios.es
     2015-09-23 19:43:25.848352+00 | fzde1XTazf | http://www.n-like.com
     2015-09-24 13:27:15.062259+00 | mKNXOLptqD | https://www.facebook.com/WorldOfRave
     2015-09-26 21:22:06.468704+00 | wTGL7E9qQJ | http://www.lilyhut.com/
     2015-09-26 22:18:34.874587+00 | ABYPd8scPG | http://cottonhoodies.net
     2015-09-27 07:43:47.261154+00 | 5t3irNTq0Y | http://www.youtube.com/watch?v=o9yIlCg88Rs
     2015-09-27 18:31:05.615092+00 | knhZG7awuF | http://www.webtoolmaster.com/it/index.htm
     2015-09-27 23:00:55.831282+00 | X9YJtf3PWb | http://placestostayinparis.net/
     2015-09-28 12:34:53.80769+00  | sdS0mL4TiW | http://customtshirtprices.com
     2015-09-30 17:05:05.897524+00 | 9WMO6W2Cs3 | http://www.youtube.com/watch?v=SrfjOIwy-tY
     2015-09-30 20:53:25.615318+00 | X9QvPV8Y8v | http://giganetwebhosting.com/wordpresshosting
     2015-10-02 15:51:18.354076+00 | OgMZX7yGo6 | http://giganetwebhosting.com/
     2015-10-03 16:14:21.959303+00 | rAotgDAd7c | http://www.youtube.com/watch?v=XI_hQup5r30
     2015-10-03 18:02:30.871545+00 | 7FyngpilnL | https://www.facebook.com/chonburiair
     2015-10-05 10:24:44.596527+00 | gOetkuXJOI | http://latarologie.sosblog.fr/index.htm
     2015-10-06 00:56:34.457558+00 | QnjJNfml7P | http://www.itunes-store-en.org
    (109 rows)

    postgres=# delete from hashes where length(long_url) <= 60 ;
    DELETE 109
    postgres=#
