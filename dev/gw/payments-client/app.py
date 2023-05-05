import logging

import uvicorn
from api.v1.subscriptions import router
from core.logger import LOGGING
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

app = FastAPI(
    docs_url="/subscriptions/api/openapi",
    openapi_url="/subscriptions/api/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    default_response_class=ORJSONResponse,
    title="API для управления своими подписками",
    description="Подписаться, сменить или удалить подписку. Посмотреть доступный подписки",
    version="1.0.0",
)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logging.info(f"{request.headers.get('x-request-id')} payments_client {request.method} {request.url}")
    response = await call_next(request)
    return response

app.include_router(router, prefix="/api/v1/subcriptions")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
