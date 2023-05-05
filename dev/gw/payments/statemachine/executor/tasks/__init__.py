import os


def init_db(engine, scoped_session_instance):
    if os.getenv('CELERY_NEEDS_SQLALCHEMY') is not None:
        if scoped_session_instance is None and engine is None:
            from executor.db.sqlalchemy import initsa
            engine, scoped_session_instance = initsa()
    return engine, scoped_session_instance
