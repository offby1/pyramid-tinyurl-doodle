#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# https://go-acme.github.io/lego/usage/cli/renew-a-certificate/

/etc/init.d/nginx stop

lego --email="eric.hanchrow@gmail.com" --domains="teensy.info" --http renew

/etc/init.d/nginx start
