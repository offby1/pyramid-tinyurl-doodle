#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

set -x

# https://go-acme.github.io/lego/usage/cli/renew-a-certificate/

/etc/init.d/nginx stop

for domain in "offby1.info" "teensy.info" "tanya-brixton.name"
do
    lego --domains=${domain} --email="eric.hanchrow@gmail.com" --http renew || lego --domains=${domain} --email="eric.hanchrow@gmail.com" --http run
done
/etc/init.d/nginx start

echo 'If "lego" comes from an ubuntu "snap", your certificates will be in /var/snap/lego/common/.lego/certificates instead of here.'
