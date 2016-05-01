tinyurl README
==================

Getting Started Locally
-----------------------

- Ensure you've got Amazon AWS config and credentials, wherever boto
  expects to find them.  See
  https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration

- cd <directory containing this file>

- cp git/post-checkout .git/hooks

- $VENV/bin/pip install -r dev-requirements.txt

- $VENV/bin/pip install -r requirements.txt

Note that the various "*requirements.txt" files, despite being checked
in to git, are automatically generated from the corresponding
"*requirements.in" files.  See https://github.com/nvie/pip-tools for
details.

- $VENV/bin/python setup.py develop

- $VENV/bin/py.test tinyurl

- $VENV/bin/pserve --reload development.ini
