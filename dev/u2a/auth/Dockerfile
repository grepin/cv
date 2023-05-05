FROM python:3.9.12-slim-buster

WORKDIR /auth/

RUN apt update &&\
    apt install -y curl gcc cmake

ADD requirements.txt /auth
RUN pip3 install -r requirements.txt

ADD / /auth

ADD /.env.docker /auth/.env

ADD /*app.py /

EXPOSE 5000/tcp


ENTRYPOINT\
        cd / &&\
        /auth/migration-upgrade.sh &&\
        /auth/migration-seed-roles.sh &&\
        gunicorn wsgi_app:app\
                --bind 0.0.0.0:5000 \
                --workers 4 \
                --log-file -
