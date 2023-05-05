from flask_jwt_extended import jwt_required

from auth.extensions.flask import app
from auth.services.user import UserService
from auth.utils.decorators import wrap_errors_in_http
from auth.utils.functional import handle
from flasgger import swag_from
from auth.docspecs.user.login import LOGIN
from auth.docspecs.user.register import REGISTER
from auth.docspecs.user.refresh import REFRESH
from auth.docspecs.user.oauth import OAUTH
from auth.docspecs.user.welcome import WELCOME
from auth.docspecs.user.update import UPDATE
from auth.docspecs.user.logout import LOGOUT
from auth.docspecs.user.terminate import TERMINATE
from auth.docspecs.user.sessions import SESSIONS


def init():
    pass


@app.route('/auth/v1/user/register', methods=['POST'])
@swag_from(specs=REGISTER)
@wrap_errors_in_http
def register():
    srv = app.service(UserService)
    return handle(srv.create, success_description='user registered')


@app.route('/auth/v1/user/update', methods=['PUT'])
@swag_from(specs=UPDATE)
@wrap_errors_in_http
@jwt_required(verify_type=True, refresh=False)
def update():
    srv = app.service(UserService)
    return handle(srv.update, success_description='user updated')


@app.route('/auth/v1/user/login', methods=['POST'])
@swag_from(specs=LOGIN)
@wrap_errors_in_http
def login():
    srv = app.service(UserService)
    return handle(srv.login, success_description='authenticated successfully')


@app.route('/auth/v1/user/oauth/<string:service>', methods=['GET'])
@swag_from(specs=OAUTH)
@wrap_errors_in_http
def oauth(service: str):
    srv = app.service(UserService)
    return handle(
        srv.oauth,
        success_description='see redirection url',
        service=service,
    )


@app.route('/auth/v1/user/oauth/<string:service>/callback', methods=['GET'])
@wrap_errors_in_http
def oauth_callback(service: str):
    srv = app.service(UserService)
    return handle(
        srv.oauth_callback,
        success_description='authenticated successfully',
        service=service,
    )


@app.route('/auth/v1/user/welcome', methods=['POST'])
@swag_from(specs=WELCOME)
@wrap_errors_in_http
def welcome():
    srv = app.service(UserService)
    return handle(srv.welcome, success_description='authenticated successfully')


@app.route('/auth/v1/user/logout', methods=['POST', 'GET'])
@swag_from(specs=LOGOUT)
@wrap_errors_in_http
@jwt_required(verify_type=True, refresh=False)
def logout():
    srv = app.service(UserService)
    return handle(srv.logout, success_description='logged out successfully')


@app.route('/auth/v1/user/terminate', methods=['POST', 'GET'])
@swag_from(specs=TERMINATE)
@wrap_errors_in_http
@jwt_required(verify_type=True, refresh=False)
def terminate():
    srv = app.service(UserService)
    return handle(srv.terminate, success_description='all sessions terminated')


@app.route('/auth/v1/user/refresh', methods=['POST', 'GET'])
@swag_from(specs=REFRESH)
@wrap_errors_in_http
@jwt_required(verify_type=True, refresh=True)
def refresh():
    srv = app.service(UserService)
    return handle(srv.refresh, success_description='tokens refreshed')


@app.route('/auth/v1/user/sessions', methods=['POST', 'GET'])
@swag_from(specs=SESSIONS)
@wrap_errors_in_http
@jwt_required(verify_type=True, refresh=False)
def sessions():
    srv = app.service(UserService)
    return handle(srv.sessions, success_description='sessions retrieved')
