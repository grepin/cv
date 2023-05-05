from flask_marshmallow import Marshmallow

from auth.extensions.flask import app

marshmallow = Marshmallow(app)
