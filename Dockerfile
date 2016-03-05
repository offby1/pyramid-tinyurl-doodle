FROM ubuntu:trusty
MAINTAINER eric.hanchrow@gmail.com

COPY sources.list /etc/apt/sources.list.d/

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip

COPY requirements.txt /tinyurl/
RUN pip3 install -r /tinyurl/requirements.txt

# This grabs our various secrets.  That wasn't intentional :-( It
# works, in that the secrets get built into the docker image, but
# they're not secret any more.  Apparently I'm not the only one with
# this sort of problem: https://github.com/docker/docker/issues/13490
# Perhaps http://square.github.io/keywhiz/ is a clean way to solve
# this.

COPY . /tinyurl/

WORKDIR /tinyurl

RUN python3 setup.py install

ENV DATABASE_URL=postgres://postgres@db:5432/postgres
ENV LC_ALL=C

CMD ["/usr/local/bin/pserve", "/tinyurl/production.ini"]
