from celery import Celery
from celery.schedules import crontab
from config import (CELERY_REDIS_DB, CELERY_REDIS_HOST, CELERY_REDIS_PASSWORD,
                    CELERY_REDIS_PORT, RMQ_HOST, RMQ_PASSWORD, RMQ_USER)

app = Celery(
    'notifications.async',
    broker='amqp://{0}:{1}@{2}'.format(RMQ_USER, RMQ_PASSWORD, RMQ_HOST),
    backend='redis://:{0}@{1}:{2}/{3}'.format(CELERY_REDIS_PASSWORD,
                                              CELERY_REDIS_HOST,
                                              CELERY_REDIS_PORT,
                                              CELERY_REDIS_DB),
    include=['tasks']
)

app.conf.beat_schedule = {
    'daily-leadership-in-notifications': {
        'task': 'tasks.daily_leadership_in_notifications',
        'schedule': crontab(hour='0', minute='30'),
    },
}
