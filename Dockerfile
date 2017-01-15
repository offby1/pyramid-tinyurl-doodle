FROM ubuntu:trusty
MAINTAINER eric.hanchrow@gmail.com

COPY sources.list /etc/apt/sources.list.d/

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip

COPY requirements.txt /tinyurl/
RUN pip3 install -r /tinyurl/requirements.txt

COPY . /tinyurl/

WORKDIR /tinyurl

RUN python3 setup.py install
RUN cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1 > .cookie_secret

ENV LC_ALL=C

CMD ["/usr/local/bin/pserve", "/tinyurl/production.ini"]
