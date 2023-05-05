FROM python:3.9.12-slim-buster

RUN mkdir /home/logs
WORKDIR /payments/api/

RUN apt update

RUN apt install -y curl
ADD requirements.txt /payments/api/
RUN pip3 install -r requirements.txt

ADD / /payments/api/
COPY filebeat-6.2.4-amd64.deb /payments/api/
RUN dpkg -i filebeat-6.2.4-amd64.deb
COPY filebeat.yml /etc/filebeat/

EXPOSE 8000/tcp

ENTRYPOINT\
        cd /payments/api/ &&\

        gunicorn main:app\
                --bind 0.0.0.0:8000 \
                -k uvicorn.workers.UvicornWorker\
                --workers 4 \
                --chdir /payments/api/ \
                --log-file - &\

        filebeat -e
