from flask_jwt_extended import jwt_required
from auth.extensions.flask import app
from auth.extensions.jwt import current_user_as_dict as jwt_current_user_data
from auth.services.role import RoleService
from auth.utils.decorators import (jwt_authorization_required,
                                   wrap_errors_in_http)
from auth.utils.functional import ExistingRoles, handle
from flasgger import swag_from
from auth.docspecs.role.list import ROLE_LIST
from auth.docspecs.role.create import ROLE_CREATE
from auth.docspecs.role.delete import ROLE_DELETE
from auth.docspecs.role.grant import ROLE_GRANT
from auth.docspecs.role.revoke import ROLE_REVOKE


def init():
    pass


@app.route('/auth/v1/role/create', methods=['POST'])
@swag_from(specs=ROLE_CREATE)
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR
    ],
    user_data_func=jwt_current_user_data
)
def create():
    srv = app.service(RoleService)
    return handle(srv.create, success_description='role created')


@app.route('/auth/v1/role/list', methods=['GET'])
@swag_from(specs=ROLE_LIST)
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR
    ],
    user_data_func=jwt_current_user_data
)
def read():
    srv = app.service(RoleService)
    return handle(srv.read, success_description='roles listed')


@app.route('/auth/v1/role/delete', methods=['DELETE'])
@swag_from(specs=ROLE_DELETE)
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR
    ],
    user_data_func=jwt_current_user_data
)
def delete():
    srv = app.service(RoleService)
    return handle(srv.delete, success_description='role deleted')


@app.route('/auth/v1/role/grant', methods=['POST'])
@swag_from(specs=ROLE_GRANT)
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR
    ],
    user_data_func=jwt_current_user_data
)
def grant():
    srv = app.service(RoleService)
    return handle(srv.grant, success_description='role granted')


@app.route('/auth/v1/role/revoke', methods=['POST'])
@swag_from(specs=ROLE_REVOKE)
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR
    ],
    user_data_func=jwt_current_user_data
)
def revoke():
    srv = app.service(RoleService)
    return handle(srv.revoke, success_description='role revoked')


@app.route('/auth/v1/role/check', methods=['POST'])
@wrap_errors_in_http
@jwt_required()
@jwt_authorization_required(
    authorized_roles=[
        ExistingRoles.EDITOR,
        ExistingRoles.SERVICE
    ],
    user_data_func=jwt_current_user_data
)
def check():
    srv = app.service(RoleService)
    return handle(srv.check, success_description='checked, allowed')
