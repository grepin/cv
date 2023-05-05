from services.utils import roles2subscription
from typing import Callable
from db.grpc import get_auth_client


class AuthService:
    def __init__(self, auth_client: Callable):
        self.auth_client = auth_client()

    async def roles(self, jwt: str):
        return await self.auth_client.whois(jwt)

    async def subscription(self, jwt: str):
        return roles2subscription(await self.roles(jwt))


def get_auth_service():
    return AuthService(get_auth_client)
