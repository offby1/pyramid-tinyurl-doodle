#!/bin/sh

/etc/init.d/nginx stop
/usr/local/bin/lego --tls --email="eric.hanchrow@gmail.com" --domains="teensy.info" --domains="www.teensy.info" --domains="tanya-brixton.name" --domains="cheyenne.demuir.name" --domains="offby1.info" --path="/etc/lego" renew
/etc/init.d/nginx start
