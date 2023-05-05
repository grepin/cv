import click

from flask.cli import AppGroup
from auth.extensions.flask import app
from auth.services.user import UserService
from auth.services.role import RoleService
from auth.utils.functional import ExistingRoles
from flask import Flask

user_cli = AppGroup('admin')
seed_cli = AppGroup('seed')


@user_cli.command('create')
@click.argument('name')
@click.argument('email')
@click.argument('password')
def create_user(name, email, password):
    with app.app_context():
        srv_user = app.service(UserService)
        user = srv_user.create({"login": name, "email": email, "password": password})
        srv_role = app.service(RoleService)
        roles = srv_role.read({})
        srv_role.grant(
            {"user_id": str(user["id"]), "role_id": str(roles['administrator'])},
            terminate=False
        )


@seed_cli.command('roles')
def insert_existing_roles():
    with app.app_context():
        srv = app.service(RoleService)
        for role in [v for k, v in vars(ExistingRoles).items() if '__' not in k]:
            srv.create({"name": role})


def init_cli(app: Flask):
    app.cli.add_command(user_cli)
    app.cli.add_command(seed_cli)
