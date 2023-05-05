import grpc

import db.user_pb2 as user_pb2
import db.user_pb2_grpc as user_pb2_grpc
from typing import Optional
from lasier.adapters.caches import AiocacheAdapter
from lasier.circuit_breaker.asyncio import circuit_breaker
from lasier.circuit_breaker.rules import MaxFailuresRule
from aiocache import Cache


class GRPCClient:
    def __init__(self, host: str, port: int):
        self.channel = grpc.aio.insecure_channel('{}:{}'.format(host, port))
        self.stub = user_pb2_grpc.userStub(self.channel)
        self.cache = AiocacheAdapter(Cache(Cache.MEMORY))
        self.rule = MaxFailuresRule(
            max_failures=0,
            failure_cache_key='c'
        )

    async def whois(self, jwt: str):
        try:
            @circuit_breaker(
                rule=self.rule,
                cache=self.cache,
                failure_timeout=30,
                failure_exception=ValueError,
                catch_exceptions=[Exception],
            )
            async def auth(jwt: str):
                response = await self.stub.whois(user_pb2.Token(jwt=jwt))
                return response.roles
            return await auth(jwt)
        except ValueError:
            pass
        return ['anonymous']

    async def close(self):
        await self.channel.close()
        await self.cache.flushdb()


auth_client: Optional[GRPCClient] = None


def get_auth_client() -> GRPCClient:
    return auth_client
