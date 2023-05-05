FROM python:3.10.8-slim-buster
RUN pip3 install --no-cache-dir celery redis python-dotenv sqlalchemy psycopg2-binary pydantic requests
WORKDIR /app
COPY . /app
ENTRYPOINT celery -A executor.app worker --loglevel INFO
