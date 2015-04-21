FROM debian:wheezy
MAINTAINER eric.hanchrow@gmail.com

COPY sources.list /etc/apt/sources.list.d/

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip 

COPY . /tinyurl/

RUN pip install -r /tinyurl/requirements.txt
RUN cd /tinyurl &&\
    python setup.py install

ENV DATABASE_URL=postgres://postgres@db:5432/postgres
ENV LC_ALL=C

CMD ["/usr/local/bin/pserve", "/tinyurl/production.ini"]
