#!/usr/bin/env python

# Hack to get some AWS config stuff into the running image.

# I should really be using IAM roles --
# http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
# (but the instance on which I currently run teensy.info wasn't
# launched with any roles, and you can't add roles to an
# already-running instance).

import os
import subprocess
import sys

server_args = [
               'docker',
               'run',
               '-p', '8000:80',
               '-v', '{}:/root/.aws:ro'.format(os.path.expanduser('~/.aws/'))
               ] + sys.argv[1:]

subprocess.call(server_args)