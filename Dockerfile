FROM python:3.6.2rc2

WORKDIR /app

ADD . /app

RUN apk add binutils libc-dev

RUN apt-get install libmysqlclient-dev && \
    pip install --upgrade pip pipenv && \
    pipenv install --system --deploy --ignore-pipfile


