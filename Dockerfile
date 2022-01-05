FROM python:3.10-alpine
RUN apk update
RUN apk add build-base libffi-dev

ADD . /app/
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
