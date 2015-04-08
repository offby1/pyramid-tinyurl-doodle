#!/bin/bash

set -e

# TODO -- only run this "apt-get update" if it's needed.  It's needed
# if and only if the "apt-get build-dep" below fails, complaining
# 
# E: You must put some 'source' URIs in your sources.list
# 
# ... which seems buggy, since there _are_ source URIs in
# /etc/apt/sources.list :-(
apt-get update

apt-get -y install postgresql python-pip python-virtualenv

apt-get -y build-dep python-psycopg2

cat > /tmp/create-user.sql <<OMG
 CREATE USER vagrant password 'vagrant';
OMG

su -c 'psql --file=/tmp/create-user.sql'     postgres 2> /dev/null

if ! su -c "psql -lqt | cut -d \| -f 1 | grep -qw vagrantwork" postgres
then
    su -c 'createdb --owner=vagrant vagrantwork' postgres
fi

cd /vagrant
if ! [ -d ~/venv ]
then
   su -c 'virtualenv ~/venv' vagrant
fi

su -c '~/venv/bin/pip install -r requirements.txt' vagrant
su -c '~/venv/bin/python setup.py develop'         vagrant

echo "Now you can do ~/venv/bin/initialize_tinyurl_db /vagrant/development.ini"
echo "and then       ~/venv/bin/pserve --reload       /vagrant/development.ini"
