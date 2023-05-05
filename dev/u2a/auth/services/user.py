import datetime
import uuid

from flask import Flask
from sqlalchemy import update

from auth.core.config import (
    JWT_FRESH_TOKEN_EXPIRES_SECONDS,
    JWT_ACCESS_TOKEN_EXPIRES_SECONDS,
    JWT_REFRESH_TOKEN_EXPIRES_SECONDS,
    JWT_ANONYMOUS_ACCESS_TOKEN_EXPIRES_SECONDS,
    JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_SECONDS
)
from auth.extensions.jwt import (current_user, gen_token,
                                 invalidate_current_token, invalidate_token,
                                 revalidate_refresh_token)
from auth.models.models import Role, Session, User
from auth.models.schemas import (SessionSchema, UserSchema, UserSchema4Login,
                                 UserSchema4Update, UserSchema4JWT)
from auth.services.mixins import CreateService, LoginService, UpdateService
from auth.utils.functional import (
    ExistingRoles,
    ActivationStatus,
    verify_password,
    make_anonymous_user,
    has_anonymous_in_roles
)
from auth.utils.http_exceptions import (
    HTTPInvalidCredentials,
    HTTPNoSuchUser,
    HTTPUnsupportedOAuthProvider,
    HTTPLoginAgain
)
from flask_jwt_extended.utils import decode_token
from auth.extensions.jwt import is_token_data_valid
from auth.extensions.jaeger import jaeger_tracing


class UserService(UpdateService, CreateService, LoginService):
    def __init__(self, app: Flask):
        self.app = app

    @staticmethod
    def _token_pair(
            user,
            fresh: int = JWT_FRESH_TOKEN_EXPIRES_SECONDS,
            access_expires: int = JWT_ACCESS_TOKEN_EXPIRES_SECONDS,
            refresh_expires: int = JWT_REFRESH_TOKEN_EXPIRES_SECONDS
    ):
        user_dict = UserSchema().dump(user)
        access_token = gen_token(
            identity=user.id,
            expires=access_expires,
            access=True,
            fresh=fresh,
            additional_claims=user_dict
        )
        refresh_token = gen_token(
            identity=user.id,
            expires=refresh_expires,
            access=False,
            additional_claims=user_dict)
        return access_token, refresh_token

    @staticmethod
    def _login_response(dump: dict, access_token: str, refresh_token: str):
        return {
            **dump,
            **{"access_token": access_token},
            **{"refresh_token": refresh_token}
        }

    def _login_user(self, user: User):
        access, refresh = UserService._token_pair(user)
        revalidate_refresh_token(actual=refresh)
        session = SessionSchema().load({
            "user_id": user.id,
            "access_token": access,
            "refresh_token": refresh
        })
        self.app.db.session.add(session)
        self.app.db.session.commit()
        return UserService._login_response(
            UserSchema().dump(user), access, refresh
        )

    @jaeger_tracing()
    def login(self, user_data: dict, **kwargs):
        validation_schema = UserSchema4Login()
        user4login = validation_schema.load(user_data, partial=True)
        user = User.query.where(User.login == user4login.login).first()
        if user is None:
            raise HTTPNoSuchUser()
        if verify_password(user4login.password, user.password) is False:
            raise HTTPInvalidCredentials()
        return self._login_user(user)

    @jaeger_tracing()
    def oauth(self, user_data: dict, **kwargs):
        provider = self.app.oauth.via(kwargs['service'])
        if provider is None:
            raise HTTPUnsupportedOAuthProvider()
        url, state = provider.authorization_data()
        return {"redirect": url}

    @jaeger_tracing()
    def oauth_callback(self, user_data: dict, **kwargs):
        provider = self.app.oauth.via(kwargs['service'])
        if provider is None:
            raise HTTPUnsupportedOAuthProvider()
        try:
            login, email = provider.handle_callback(kwargs['code'])
        except Exception:
            raise HTTPLoginAgain()
        user = User.query.filter_by(email=email).first()
        if user is None:
            self.create(user_data={
                'login': login,
                'email': email,
                'password': str(uuid.uuid4())
            }, active=ActivationStatus.OAUTH_REGISTRATION_ACTIVE)
            user = User.query.filter_by(email=email).first()
        return self._login_user(user)

    @jaeger_tracing()
    def update(self, user_data: dict, **kwargs):
        user = current_user()
        if has_anonymous_in_roles(user):
            return UserSchema4JWT().dump(user)
        validation_schema = UserSchema4Update()
        user4update = validation_schema.load(
            user_data, partial=True)
        statement = update(UserSchema.Meta.model) \
            .where(UserSchema.Meta.model.id == current_user().id) \
            .values(validation_schema.dump(user4update)) \
            .returning("*")
        user = self.app.db.session.execute(statement).first()
        return validation_schema.dump(user)

    @jaeger_tracing()
    def create(self, user_data: dict, **kwargs):
        schema = UserSchema()
        user = schema.load(user_data)
        if 'active' in kwargs:
            user.active = kwargs['active']
        else:
            user.active = ActivationStatus.DIRECT_REGISTRATION_ACTIVE
        subscriber_role = Role.query.filter_by(name=ExistingRoles.USER).first()
        user.roles.append(subscriber_role)
        self.app.db.session.add(user)
        self.app.db.session.commit()
        user = User.query.join(User.roles).where(User.id == user.id).first()
        return schema.dump(user)

    @jaeger_tracing()
    def logout(self, user_data: dict, **kwargs):
        user = current_user()
        if has_anonymous_in_roles(user) is False:
            invalidate_current_token()
        return {}

    @jaeger_tracing()
    def do_terminate(self):
        user = current_user()
        if has_anonymous_in_roles(user):
            return
        for acesss, refresh in self.app.db.session.query(
                Session.access_token, Session.refresh_token).filter(
                    Session.user_id == user.id,
                    Session.expires > datetime.datetime.utcnow()
        ).yield_per(1):
            invalidate_token(acesss)
            invalidate_token(refresh)

    @jaeger_tracing()
    def terminate(self, user_data: dict, **kwargs):
        self.do_terminate()
        return {}

    def _get_anonymous_tokens(self, anonymous):
        access, refresh = UserService._token_pair(
            anonymous,
            access_expires=JWT_ANONYMOUS_ACCESS_TOKEN_EXPIRES_SECONDS,
            refresh_expires=JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_SECONDS
        )
        return {
            "access_token": access,
            "refresh_token": refresh
        }

    @jaeger_tracing()
    def refresh(self, user_data: dict, **kwargs):
        user = current_user()
        if has_anonymous_in_roles(user):
            return self._get_anonymous_tokens(user)
        invalidate_current_token()
        access, refresh = UserService._token_pair(user)
        session = SessionSchema().load({
            "user_id": user.id,
            "access_token": access,
            "refresh_token": refresh
        })
        self.app.db.session.add(session)
        self.app.db.session.commit()
        return {
            "access_token": access,
            "refresh_token": refresh
        }

    @jaeger_tracing()
    def sessions(self, user_data: dict, **kwargs):
        user = current_user()
        schema = SessionSchema(many=True)
        sessions = []
        if has_anonymous_in_roles(user) is False:
            sessions = schema.Meta.model.query.filter_by(user_id=current_user().id).all()
        return schema.dump(sessions)

    @jaeger_tracing()
    def welcome(self, user_data: dict, **kwargs):
        anonymous = UserSchema4JWT().load(make_anonymous_user(), partial=True)
        anonymous.roles.append(Role(id=uuid.uuid4(), name=ExistingRoles.ANONYMOUS))
        tokens = self._get_anonymous_tokens(anonymous)
        return tokens

    def whois(self, user_data, **kwargs):
        error_response = [ExistingRoles.ANONYMOUS]
        if 'jwt' not in kwargs:
            return error_response
        try:
            jwt_data = decode_token(encoded_token=kwargs['jwt'])
        except Exception:
            return error_response
        if 'roles' not in jwt_data:
            return error_response
        if not is_token_data_valid(jwt_data):
            return error_response
        return jwt_data['roles']
