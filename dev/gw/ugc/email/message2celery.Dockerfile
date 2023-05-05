FROM python:3.10.8-slim-buster
RUN pip3 install --no-cache-dir celery redis python-dotenv pika pymongo jinja2
WORKDIR /app
COPY . .
ENTRYPOINT python3 message2celery.py
