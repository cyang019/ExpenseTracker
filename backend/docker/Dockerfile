FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/code
RUN mkdir /opt/requirements
WORKDIR /opt/code

ADD requirements /opt/requirements
RUN pip install -r /opt/requirements/development.txt

ADD application /opt/application
ADD config /opt/config
ADD migrations /opt/migrations
ADD .env /opt/.env
