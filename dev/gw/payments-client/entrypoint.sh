#!/bin/bash
service filebeat start
python -m gunicorn app:app --workers 5 --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8080
