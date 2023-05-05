from flask import Flask
from sqlalchemy.orm.strategy_options import Load

from auth.models.models import Role, User, User2Role
from auth.models.schemas import Role4Check, RoleSchema, User2RoleSchema
from auth.services.mixins import CreateService, DeleteService, ReadService
from auth.services.user import UserService
from auth.utils.functional import ExistingRoles
from auth.utils.http_exceptions import (HTTPNoSuchGrant, HTTPRoleHasUsers,
                                        HTTPRoleNotExists, HTTPUndeletableRole)
from auth.extensions.jaeger import jaeger_tracing


class RoleService(CreateService, ReadService, DeleteService):
    def __init__(self, app: Flask):
        self.app = app

    @jaeger_tracing()
    def create(self, data: dict, **kwargs):
        schema = RoleSchema()
        role = schema.load(data)
        self.app.db.session.add(role)
        self.app.db.session.commit()
        return schema.dump(role)

    @jaeger_tracing()
    def read(self, data: dict, **kwargs):
        schema = RoleSchema()
        return schema.dump(Role.query.options(Load(Role).lazyload('*')).all())

    @jaeger_tracing()
    def delete(self, data: dict, **kwargs):
        existing_roles = [
            v for k, v in vars(ExistingRoles).items() if '__' not in k
        ]
        schema = RoleSchema()
        role = schema.load(data, partial=('id',), session=self.app.db.session)
        role = Role.query.filter_by(name=role.name).first()
        if role is None:
            raise HTTPRoleNotExists()
        if role.name in existing_roles:
            raise HTTPUndeletableRole()
        role = Role.query.filter_by(name=role.name).first()
        if hasattr(role, 'users') and len(role.users) > 0:  # TODO: заменить на count(1)
            raise HTTPRoleHasUsers()
        self.app.db.session.delete(role)
        self.app.db.session.commit()
        return schema.dump(role)

    @jaeger_tracing()
    def grant(self, data: dict, **kwargs):
        schema = User2RoleSchema()
        u2r = schema.load(data, partial=('id',), session=self.app.db.session)
        self.app.db.session.add(u2r)
        self.app.db.session.commit()
        if not ('terminate' in kwargs and kwargs['terminate'] is False):
            self.app.service(UserService).do_terminate()  # грязный хак
        return schema.dump(u2r)

    @jaeger_tracing()
    def revoke(self, data: dict, **kwargs):
        schema = User2RoleSchema()
        u2r = schema.load(data, partial=('id',), session=self.app.db.session)
        u2r = User2Role.query.filter_by(user_id=u2r.user_id, role_id=u2r.role_id).first()
        if u2r is None:
            raise HTTPNoSuchGrant()
        self.app.db.session.delete(u2r)
        self.app.db.session.commit()
        self.app.service(UserService).do_terminate()  # грязный хак
        return schema.dump(u2r)

    @jaeger_tracing()
    def check(self, data: dict, **kwargs):
        schema = Role4Check()
        chk = schema.load(data)
        user = User.query.filter_by(id=chk.id).first()
        if user is None:
            raise HTTPNoSuchGrant()  # anonymous-совместимость
        if chk.name not in [role.name for role in user.roles]:
            raise HTTPNoSuchGrant()
        return {}
