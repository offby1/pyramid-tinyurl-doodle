#!/bin/bash
set -euo pipefail
# something something folders
mkdir -p /var/lib/mysql
mkdir -p /var/lib/nginx
mkdir -p /var/log
mkdir -p /var/log/mysql
mkdir -p /var/log/nginx
# Wipe /var/run, since pidfiles and socket files from previous launches should go away
# TODO someday: I'd prefer a tmpfs for these.
rm -rf /var/run
mkdir -p /var/run
mkdir -p /var/run/mysqld

UWSGI_SOCKET_FILE=/var/run/uwsgi.sock

# Ensure mysql tables created
HOME=/etc/mysql /usr/bin/mysql_install_db --force

# Spawn mysqld
HOME=/etc/mysql /usr/sbin/mysqld &

MYSQL_SOCKET_FILE=/var/run/mysqld/mysqld.sock
# Wait for mysql to bind its socket
while [ ! -e $MYSQL_SOCKET_FILE ] ; do
    echo "waiting for mysql to be available at $MYSQL_SOCKET_FILE"
    sleep .2
done

# Initialize db
echo "CREATE DATABASE IF NOT EXISTS app; GRANT ALL on app.* TO 'app'@'localhost' IDENTIFIED BY 'app';" | mysql -uroot
/opt/app/env/bin/initialize_tinyurl_db /opt/app/sandstorm.ini

# Spawn uwsgi
HOME=/var uwsgi \
        --socket $UWSGI_SOCKET_FILE \
        --plugin python \
        --virtualenv /opt/app/env \
        --paste config:///opt/app/sandstorm.ini &

# Wait for uwsgi to bind its socket
while [ ! -e $UWSGI_SOCKET_FILE ] ; do
    echo "waiting for uwsgi to be available at $UWSGI_SOCKET_FILE"
    sleep .2
done

# Start nginx.
/usr/sbin/nginx -g "daemon off;"

