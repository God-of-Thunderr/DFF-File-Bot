FROM python:3.8-slim-buster

FROM debian:latest

# basic
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN 

# basic
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN python3 -m pip install -U pip

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /EvaMaria
WORKDIR /EvaMaria
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
