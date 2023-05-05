from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from auth.core.config import JWT_ACCESS_TOKEN_EXPIRES_SECONDS
from auth.extensions.postgres import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(),
                   unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=True)
    lastname = db.Column(db.String, unique=False, nullable=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Integer, nullable=False, default=0)
    roles = db.relationship('Role', secondary='user2role', back_populates='users')


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), unique=True,
                   nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship('User', secondary='user2role', back_populates='roles')


class User2Role(db.Model):
    __tablename__ = 'user2role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), unique=True,
                   nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='ur'),)


def access_expiration():
    return datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES_SECONDS)


class Session(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('user_id', 'id'),
        {'postgresql_partition_by': 'HASH(user_id, id)'},
    )

    id = db.Column(UUID(as_uuid=True), server_default=func.uuid_generate_v4(), unique=False, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), unique=False, nullable=False)
    logon_date = db.Column(db.DateTime(timezone=False), nullable=False, unique=False, server_default=func.now())
    expires = db.Column(db.DateTime(timezone=False), nullable=False, unique=False, default=access_expiration)
    access_token = db.Column(db.String, unique=False, nullable=False)
    refresh_token = db.Column(db.String, unique=False, nullable=False)
