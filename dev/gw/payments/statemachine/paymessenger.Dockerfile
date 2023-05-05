FROM python:3.10.8-slim-buster
RUN pip3 install --no-cache-dir celery redis python-dotenv pika sqlalchemy pydantic
WORKDIR /app
COPY . /app
ENTRYPOINT python3 paymessenger.py
