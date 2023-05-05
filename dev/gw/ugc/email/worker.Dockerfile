FROM python:3.10.8-slim-buster
RUN pip3 install --no-cache-dir celery redis python-dotenv pymongo jinja2
WORKDIR /app
COPY . .
ENTRYPOINT celery -A app worker --beat --loglevel INFO
