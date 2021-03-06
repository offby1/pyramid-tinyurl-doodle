FROM ubuntu:focal
MAINTAINER eric.hanchrow@gmail.com

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pipenv git

COPY Pipfile /tinyurl/
COPY Pipfile.lock /tinyurl/

COPY . /tinyurl/

WORKDIR /tinyurl

ENV AWS_DEFAULT_REGION=us-west-1
ENV LANG=C
ENV LC_ALL=C
ENV PIPENV_VENV_IN_PROJECT=true

RUN python3 -m pipenv sync
RUN python3 -m pipenv run python3 setup.py install
RUN cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

CMD ["python3", "-m", "pipenv", "run", "python3", "/tinyurl/.venv/bin/pserve", "/tinyurl/production.ini"]
