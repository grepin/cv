import hashlib
import smtplib
from datetime import datetime, timedelta

from app import app
from config import (EMAIL_PASSWORD, EMAIL_USER, MONGO_DB, MONGO_DSN,
                    MONGO_NOTIFICATION_COLLECTION)
from mailproducer import html_message
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

mongo_client = None
mongo_db = None
mongo_collection = None


def mongo():
    global mongo_db, mongo_collection, mongo_client
    if mongo_client is None:
        mongo_client = MongoClient(MONGO_DSN)
        mongo_db = mongo_client[MONGO_DB]
        mongo_collection = mongo_db[MONGO_NOTIFICATION_COLLECTION]


def update_status(notification_id: str, status: str):
    mongo()
    return mongo_collection.find_one_and_update(
        filter={'notification_id': notification_id},
        update={'$set': {'status': status}},
        upsert=False,
        return_document=ReturnDocument.BEFORE
    )


def insert_once(notification_id: str, doc: dict):
    mongo()
    return mongo_collection.find_one_and_update(
        filter={'notification_id': notification_id},
        update={'$setOnInsert': doc},
        upsert=True,
        return_document=ReturnDocument.BEFORE
    )


def daily_leaders():
    mongo()
    leaders = [
        {"$match": {"created": {"$gt": str(datetime.now() - timedelta(days=1))}}},
        {"$group": {"_id": "$email", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(mongo_collection.aggregate(leaders))


def gmail(message) -> bool:
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(
            message['From'],
            message['To'],
            message.as_string()
        )
        server.close()
    except Exception:
        return False
    return True


@app.task(
    bind=True,
    autoretry_for=(AssertionError,),
    retry_backoff=15,
    max_retries=5,
    retry_jitter=False,
)
def sendmail(self, json: dict) -> None:
    doc = update_status(json['notification_id'], 'processing')
    status = doc['status']
    if (status == 'completed') or (status == 'processing' and self.request.retries == 0):
        return
    email = html_message(
        EMAIL_USER,
        json['email'],
        json['subject'],
        'message-subject.html',
        title=json['subject'],
        text=json['message'],
        image='https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
    )
    sent = gmail(email)
    if sent is True:
        doc = update_status(json['notification_id'], 'completed')
    else:
        if self.request.retries == self.max_retries:
            doc = update_status(json['notification_id'], 'failed')
        else:
            raise AssertionError


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=15,
    max_retries=5,
    retry_jitter=False,
)
def daily_leadership_in_notifications(self):
    leaders = daily_leaders()
    for leader in leaders[:10]:
        if '_id' in leader and 'count' in leader:
            base = leader['_id'] + datetime.today().strftime("%d/%m/%Y")
            task_rerun_tolerant_notification_id = \
                'dlin-' + hashlib.md5(base.encode('utf-8')).hexdigest()
            json = {
                "message_id": task_rerun_tolerant_notification_id,
                "email": leader["_id"],
                "notification_id": task_rerun_tolerant_notification_id,
                "status": "generated",
                "subject": "you're a true leader and eligable for a bonus!",
                "created": str(datetime.now()),
                "message": """
                It's not easy to become a true leader, {0}, but you've made it today!.
                Your notifications count for today is {1}, which makes you one of
                our messaging champions. Feel free to continue and get the absolute
                leader $10.000 bonus one day!
                """.format(leader['_id'], leader['count'])
            }
            if insert_once(task_rerun_tolerant_notification_id, json) is None:
                sendmail.apply_async(
                    args=[json],
                    task_id=json['notification_id'],
                )
