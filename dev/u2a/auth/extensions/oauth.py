import abc
from abc import ABCMeta
from requests_oauthlib import OAuth2Session
from auth.extensions.flask import app
from auth.core.config import (
    OAUTH_CALLBACK_PREFIX,
    OAUTH_CALLBACK_POSTFIX,
    OAUTH_YANDEX_ID,
    OAUTH_YANDEX_SECRET,
    OAUTH_YANDEX_URL,
    OAUTH_YANDEX_TOKEN_URL,
    OAUTH_YANDEX_INFO_URL
)


class OAuth2Service(metaclass=ABCMeta):

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def authorization_data(self) -> tuple:
        pass

    @abc.abstractmethod
    def handle_callback(self):
        pass


class OAuthAuthorization:
    def __init__(self):
        self.providers = {}

    def register(self, provider: OAuth2Service) -> None:
        self.providers[provider.name()] = provider

    def via(self, name: str) -> OAuth2Service:
        if name in self.providers:
            return self.providers[name]
        return None


class YandexOAuth2WebFlow(OAuth2Service):
    SCOPE = ["login:email", "login:info"]
    SERVICE_NAME = 'yandex'
    PROVIDER_OAUTH2_URL = OAUTH_YANDEX_URL
    PROVIDER_TOKEN_URL = OAUTH_YANDEX_TOKEN_URL
    PROVIDER_INFO_URL = OAUTH_YANDEX_INFO_URL

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            callback_prefix: str,
            callback_postfix: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = "{}{}{}".format(
            callback_prefix,
            self.SERVICE_NAME,
            callback_postfix
        )
        self.oauth = OAuth2Session(
            client_id=self.client_id,
            scope=self.SCOPE,
            redirect_uri='{}{}{}'.format(
                callback_prefix,
                YandexOAuth2WebFlow.SERVICE_NAME,
                callback_postfix
            )
        )
        self.token = None

    def name(self):
        return self.SERVICE_NAME

    def authorization_data(self):
        authorization_url, state = self.oauth.authorization_url(
            self.PROVIDER_OAUTH2_URL,
        )
        return authorization_url, state

    def handle_callback(self, code):
        token = self.oauth.fetch_token(
            token_url=self.PROVIDER_TOKEN_URL,
            code=code,
            include_client_id=self.client_id,
            client_secret=self.client_secret
        )
        user_data = self.oauth.get(
            self.PROVIDER_INFO_URL,
            headers={'Authorization': 'OAuth {}'.format(token)}
        ).json()
        return user_data['login'], user_data['default_email']


def init(app):
    oa = OAuthAuthorization()
    app.config['OAUTH_CALLBACK_PREFIX'] = OAUTH_CALLBACK_PREFIX
    app.config['OAUTH_CALLBACK_POSTFIX'] = OAUTH_CALLBACK_POSTFIX
    oa.register(
        YandexOAuth2WebFlow(
            client_id=OAUTH_YANDEX_ID,
            client_secret=OAUTH_YANDEX_SECRET,
            callback_prefix=OAUTH_CALLBACK_PREFIX,
            callback_postfix=OAUTH_CALLBACK_POSTFIX,
        )
    )
    return oa


oauth = init(app)
