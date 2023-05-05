import os

from celery import Celery
from core.config import settings


def init():
    path = os.path.dirname(__file__) + '/tasks/'
    i = ['executor.tasks.' + f[:-3] for f in os.listdir(path) if '__' not in f and f.endswith('.py')]
    a = Celery(
        'notifications.async',
        broker='amqp://{0}:{1}@{2}'.format(
            settings.RMQ_USER,
            settings.RMQ_PASSWORD,
            settings.RMQ_HOST),
        backend='redis://:{0}@{1}:{2}/{3}'.format(settings.CELERY_REDIS_PASSWORD,
                                                  settings.CELERY_REDIS_HOST,
                                                  settings.CELERY_REDIS_PORT,
                                                  settings.CELERY_REDIS_PAYMENTS_DB),
        include=list(i)
    )
    a.conf.task_default_queue = 'celery4payments'
    return a


app = init()
