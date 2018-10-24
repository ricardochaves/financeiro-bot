FROM python:3.6.2rc2
ENV PYTHONUNBUFFERED 1

LABEL maintainer "ricardo.chaves@infoglobo.com.br"

EXPOSE 3000 5005

RUN mkdir /base_site
WORKDIR /base_site

ADD . /base_site

RUN chmod +x ./base_site.sh

RUN apt-get install libmysqlclient-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements_dev.txt


