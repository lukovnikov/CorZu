FROM ubuntu:16.04

RUN apt-get update && apt-get -y install \
    git \
    swi-prolog \
    sfst \
    unzip \
    wget \
    python \
    python-pexpect \
    python-flask

RUN git clone https://github.com/lukovnikov/ParZu

RUN (cd ParZu; bash install.sh)

WORKDIR /ParZu
CMD python parzu_server.py -p 5678 -H 0.0.0.0
