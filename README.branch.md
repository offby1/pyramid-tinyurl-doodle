Looks like sandstorm has only a few built-in "stacks", and none of
them are "pyramid", so I gotta either use the "diy" stack, which is
probably hard; or else "port" this to some other stack.
[The "uwsgi" stack](https://github.com/sandstorm-io/vagrant-spk/tree/master/stacks/uwsgi)
seems roughly what I'd want.

So ... it apparently requires mysql, so the first order of business:
port to mysql.  Shouldn't be hard.

* uwsgi

    uwsgi seems quite complex, but I stumbled onto a formula that seems to work (on Ubuntu "trusty"):

        $ sudo aptitude install python-pip
        $ pip3 install --user virtualenv
        $ ~/.local/bin/virtualenv venv.$(uname -s)
        $ source venv.$(uname -s)/bin/activate
        (venv.Linux)$ pip install -r requirements.txt
        (venv.Linux)$ pip install uwsgi
        (venv.Linux)$ python setup.py develop
        (venv.Linux)$ initialize_tinyurl_db development.ini
        (venv.Linux)$ uwsgi --paste config://$(pwd)/development.ini  --http 0.0.0.0:6543

    Since the above appears to work, and didn't require me to change any
    of the app's code, I hereby pronounce the app to be uwsgi-ready.

* mysql

    Do the below in a "trusty" Vagrant box: 
        
        $ sudo aptitude install python-dev libmysqlclient-dev mysql-server # set root password to "root" when prompted
        $ mysql -u root -proot -e 'create database if not exists tinyurl'
        $ source venv.$(uname -s)/bin/activate
        (venv.Linux)$ pip install -r requirements.txt
        (venv.Linux)$ python setup.py develop
        (venv.Linux)$ initialize_tinyurl_db development.ini
        (venv.Linux)$ uwsgi --paste config://$(pwd)/development.ini  --http 0.0.0.0:6543

* sandstorm!!

    Following along
    [the tutorial](https://docs.sandstorm.io/en/latest/vagrant-spk/customizing/),
    do this on this very machine:
        
        $ vagrant-spk setupvm uwsgi
        $ vagrant-spk up
... long pause...

        $ vagrant-spk init
        $ vagrant-spk dev 

