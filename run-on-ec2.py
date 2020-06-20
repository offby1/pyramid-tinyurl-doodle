#!/usr/bin/env python

# Hack to get some AWS config stuff into the running image.

# I should really be using IAM roles --
# http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
# (but the instance on which I currently run teensy.info wasn't
# launched with any roles, and you can't add roles to an
# already-running instance).

# TODO -- investigate "Fargate", which is (perhaps) an easy way to run containerized apps.
# https://www.learnaws.org/2018/02/06/Introduction-AWS-Fargate/ is a very brief tutorial.
import os
import subprocess
import sys

server_args = [
    "docker",
    "run",
    "-p",
    "8080:8080",
] + sys.argv[1:]

subprocess.run(server_args)
