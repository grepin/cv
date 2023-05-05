import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis, grpc


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании кинопроизведений",
    version="1.0.0"
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT),
        db=config.REDIS_DB,
        password=config.REDIS_PASSWORD,
        minsize=10,
        maxsize=20
    )
    elastic.es = AsyncElasticsearch(
        hosts=eval(config.ELASTICSEARCH_ADDRESS)
    )
    grpc.auth_client = grpc.GRPCClient(
        host=config.GRPC_SERVER_HOST,
        port=config.GRPC_SERVER_PORT
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()
    await grpc.auth_client.close()


app.include_router(films.router, prefix='/api/v1/films')
app.include_router(genres.router, prefix='/api/v1/genres')
app.include_router(persons.router, prefix='/api/v1/persons')


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
