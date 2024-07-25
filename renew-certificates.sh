#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# https://go-acme.github.io/lego/usage/cli/renew-a-certificate/

/etc/init.d/nginx stop

lego                                            \
    --email="eric.hanchrow@gmail.com"           \
    --domains="offby1.info"                     \
    --domains="teensy.info"                     \
    --domains="www.teensy.info"                 \
    --domains="eensy.teensy.info"               \
    --domains="tanya-brixton.name"              \
    --http run

/etc/init.d/nginx start

echo 'If "lego" comes from an ubuntu "snap", your certificates will be in /var/snap/lego/common/.lego/certificates instead of here.'
