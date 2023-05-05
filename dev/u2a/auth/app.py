from flask import Flask
import auth.routes.role
import auth.routes.user
from auth.extensions.flask import app as flask_app
from auth.extensions.jwt import jwt
from auth.extensions.marshmallow import marshmallow
from auth.extensions.postgres import db
from auth.extensions.flassger import flassger
from auth.extensions.redis import redis4access, redis4refresh, redis4rate_limiter
from auth.extensions.oauth import oauth
from auth.extensions.jaeger import jaeger_init
from auth.extensions.ratelimiter import init_rate_limiter
from auth.extensions.cli import init_cli
from auth.services.role import RoleService
from auth.services.user import UserService
from auth.utils.functional import jsonify_wrapper
from auth.extensions.migrate import init_migration


def register_services(flask: Flask, *service_classes):
    flask.srv = {}
    for service_class in service_classes:
        flask.srv[service_class.__name__] = service_class(flask)
    flask.service = lambda x: flask.srv[x.__name__]


def init(app: Flask):
    app.db = db
    app.marshmallow = marshmallow
    app.jwt = jwt
    app.redis4refresh = redis4refresh
    app.redis4access = redis4access
    app.redis4rate_limiter = redis4rate_limiter
    app.flassger = flassger
    app.oauth = oauth
    app.tracer = jaeger_init()
    app.rate_limiter = init_rate_limiter(app.redis4rate_limiter, app)
    app.migrate = init_migration(app)
    init_cli(app)
    auth.routes.role.init()
    auth.routes.user.init()
    register_services(
        app,
        UserService,
        RoleService
    )
    return app


app = init(flask_app)


@app.errorhandler(Exception)
def on_exception(e):
    return jsonify_wrapper(
        description=e.description if hasattr(e, 'description') else 'internal error: ' + str(e),
        data=e.data if hasattr(e, 'data') else {},
        success=False,
        code=e.code if hasattr(e, 'code') else 500)


def main():
    app.run()


if __name__ == '__main__':
    main()
