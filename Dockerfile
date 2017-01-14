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

ENV LC_ALL=C

CMD ["/usr/local/bin/pserve", "/tinyurl/production.ini"]
