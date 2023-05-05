from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import (post_dump, post_load, pre_dump, pre_load, validate,
                         validates)

from auth.models.models import Role, Session, User, User2Role
from auth.utils.functional import generate_password
from auth.utils.http_exceptions import (HTTPExcessiveField,
                                        HTTPFieldModificationProhibited,
                                        HTTPMissingField)


class UserSchemaPasswordDumpScreening:
    @post_dump(pass_many=False)
    def remove_password(self, data, many, **kwargs):
        if data is not None:
            if 'password' in data:
                data.pop('password')
        return data


class UserSchemaValidation:
    @validates('login')
    def validate_login(self, data, **kwargs):
        validate.Regexp(r'[a-zA-Z0-9_-]{3,32}')(data)

    @validates('email')
    def validate_email(self, data, **kwargs):
        validate.Email()(data)

    @validates('name')
    def validate_name(self, data, **kwargs):
        if data is not None:
            validate.Regexp(r'[a-zA-Z0-9_-]{1,128}')(data)

    @validates('lastname')
    def validate_lastname(self, data, **kwargs):
        if data is not None:
            validate.Regexp(r'[a-zA-Z0-9_-]{1,128}')(data)

    @validates('password')
    def validate_password(self, data, **kwargs):
        validate.Regexp(r'[a-zA-Z0-9_\-!@#]{8,128}')(data)


class UserSchema(
    SQLAlchemyAutoSchema,
    UserSchemaValidation,
    UserSchemaPasswordDumpScreening
):
    assigned_roles = {}

    class Meta:
        model = User
        load_instance = True

    @post_load(pass_many=False)
    def cleanup(self, data, many, **kwargs):
        if data is not None:
            if 'active' in data:
                data.pop('active')
            data['password'] = generate_password(data['password'])
        return data

    @pre_dump(pass_many=False)
    def rebuild(self, data, many, **kwargs):
        assigned_roles = {}
        if data.roles is not None:
            assigned_roles = {role.name: role.id for role in data.roles}
        self.assigned_roles = assigned_roles
        return data

    @post_dump(pass_many=False)
    def roles(self, data, many, **kwargs):
        data['roles'] = self.assigned_roles
        return data


class UserSchema4Update(
    SQLAlchemyAutoSchema,
    UserSchemaValidation,
    UserSchemaPasswordDumpScreening
):
    allowed2change = ['login', 'email', 'name', 'lastname', 'password']

    class Meta:
        model = User
        load_instance = True
        transient = True

    @pre_load(pass_many=False)
    def modify_structure(self, data, many, **kwargs):
        if data is not None:
            for key in list(data.keys()):
                if key not in self.allowed2change:
                    raise HTTPFieldModificationProhibited(data={key: ["modification prohibited"]})
        return data

    @post_dump(pass_many=False)
    def cleanup(self, data, many, **kwargs):
        if data is not None:
            for key in list(data.keys()):
                if key not in self.allowed2change or data[key] is None:
                    data.pop(key)
        return data


class UserSchema4Login(
    SQLAlchemyAutoSchema,
    UserSchemaValidation,
    UserSchemaPasswordDumpScreening
):
    class Meta:
        model = User
        load_instance = True
        transient = True

    @pre_load(pass_many=False)
    def modify_structure(self, data, many, **kwargs):
        needed = ['login', 'password']
        if data is not None:
            for key in list(data.keys()):
                if key not in needed:
                    raise HTTPExcessiveField(data={key: ["not needed"]})
        for key in needed:
            if key not in data.keys():
                raise HTTPMissingField(data={key: ["missing"]})
        return data


class UserSchema4JWT(
    SQLAlchemyAutoSchema,
    UserSchemaValidation,
    UserSchemaPasswordDumpScreening
):
    assigned_roles = {}

    class Meta:
        model = User
        load_instance = True
        transient = True

    @pre_load(pass_many=False)
    def modify_structure(self, data, many, **kwargs):
        allowed = ['login', 'active', 'lastname', 'id', 'name', 'email', 'roles']
        if data is not None:
            if 'roles' in data:
                roles = data.pop('roles')
                self.assigned_roles = roles
            for key in list(data.keys()):
                if key not in allowed:
                    data.pop(key)
        return data


class SessionSchema(
    SQLAlchemyAutoSchema,
):
    class Meta:
        model = Session
        load_instance = True

    @post_dump(pass_many=True)
    def format(self, data, many, **kwargs):
        if data is None:
            data = []
        for i in data:
            visible = ['logon_date', 'access_token', 'expires']
            for key in list(i.keys()):
                if key not in visible:
                    i.pop(key)
        return {
            "count": len(data),
            "sessions": data
        }


class RoleSchemaValidation:
    @validates('name')
    def validate_login(self, data, **kwargs):
        validate.Regexp(r'[a-zA-Z0-9_-]{3,128}')(data)


class RoleSchema(
    SQLAlchemyAutoSchema,
    RoleSchemaValidation,
):
    class Meta:
        model = Role
        load_instance = True

    @post_dump(pass_many=True, pass_original=True)
    def post_many(self, data, original, many, **kwargs):
        if type(original) is list:
            data = {role.name: role.id for role in original}
        else:
            data = {original.name: original.id}
        return data


class User2RoleSchema(SQLAlchemyAutoSchema):
    uuid_regex = r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$'

    class Meta:
        model = User2Role
        load_instance = True
        include_fk = True

    @validates('role_id')
    def validate_role_id(self, data, **kwargs):
        validate.Regexp(r'[a-zA-Z0-9_-]{3,128}')(str(data))

    @validates('user_id')
    def validate_user_id(self, data, **kwargs):
        validate.Regexp(r'[a-zA-Z0-9_-]{3,128}')(str(data))


class Role4Check(
    SQLAlchemyAutoSchema,
    RoleSchemaValidation,
):
    class Meta:
        model = Role
        load_instance = True
        transient = True
