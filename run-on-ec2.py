#!/usr/bin/env python

# Hack to get some AWS config stuff into the running image.  I'm sure
# there's a better way, but this works.

import configparser
import os
import subprocess
import sys

c = configparser.ConfigParser ()
c.read (os.path.expanduser('~/.aws/credentials'))

server_args = [
               'docker',
               'run',
               '-p', '8000:80',
               '--env', 'AWS_ACCESS_KEY_ID={}'.format (c['default']['aws_access_key_id']),
               '--env', 'AWS_DEFAULT_REGION=us-west-1',
               '--env', 'AWS_SECRET_ACCESS_KEY={}'.format (c['default']['aws_secret_access_key']),
               ] + sys.argv[1:]

subprocess.call(server_args)
