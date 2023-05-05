import logging

import uvicorn
from api.v1 import cancel, paid, pay, repay
from core.config import LOGGING, settings
from db import rabbitmq
from db.rabbitmq import RabbitMQ
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    title="API интеграции через платежные виджеты внешних провайдеров",
    description="Функции для работы через платежные виджеты, предоставляемые шлюзами/агрегаторами",
    version="1.0.0"
)


@app.on_event('startup')
async def statup():
    rabbitmq.rmq = RabbitMQ(
        user=settings.RMQ_USER,
        host=settings.RMQ_HOST,
        password=settings.RMQ_PASSWORD,
        exchange=settings.RMQ_PAYMENTS_EXCHANGE,
        routing_key=settings.RMQ_PAYMENTS_ROUTING_KEY
    )
    rabbitmq.rmq.start()


@app.on_event('shutdown')
async def shutdown():
    rabbitmq.rmq.stop()


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logging.info(f"{request.headers.get('x-request-id')} payments_api {request.method} {request.url}")
    response = await call_next(request)
    return response


app.include_router(pay.router, prefix='/api/v1/pay')
app.include_router(paid.router, prefix='/api/v1/paid')
app.include_router(cancel.router, prefix='/api/v1/cancel')
app.include_router(repay.router, prefix='/api/v1/repay')

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=settings.LOGGING,
        log_level=logging.DEBUG
    )
