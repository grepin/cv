import os

from dotenv import load_dotenv

load_dotenv()

CELERY_REDIS_HOST = os.getenv('CELERY_REDIS_HOST')
CELERY_REDIS_PORT = int(os.getenv('CELERY_REDIS_PORT', 6379))
CELERY_REDIS_PASSWORD = os.getenv('CELERY_REDIS_PASSWORD')
CELERY_REDIS_DB = int(os.getenv('CELERY_REDIS_DB', 5))
RMQ_HOST = os.getenv('RMQ_HOST')
RMQ_USER = os.getenv('RMQ_USER', 'guest')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'guest')
RMQ_EMAIL_EXCHANGE = os.getenv('RMQ_EMAIL_EXCHANGE', 'aqm.direct')
RMQ_EMAIL_QUEUE = os.getenv('RMQ_EMAIL_QUEUE', 'email.notification')
RMQ_EMAIL_ROUTING_KEY = os.getenv('RMQ_EMAIL_ROUTING_KEY', 'email.notification')
MONGO_DSN = os.getenv('MONGO_DSN')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_NOTIFICATION_COLLECTION = os.getenv('MONGO_NOTIFICATION_COLLECTION')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
