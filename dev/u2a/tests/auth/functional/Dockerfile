FROM python:3.9.12-slim-buster

WORKDIR /

ADD tests/auth/functional/requirements.txt /

RUN pip3 install -r requirements.txt

ADD / /

ENTRYPOINT\
        cat .env &&\
        pytest -vv tests/auth/functional/src

