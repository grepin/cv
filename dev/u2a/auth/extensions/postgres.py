from flask_sqlalchemy import SQLAlchemy

from auth.core.config import (SQLALCHEMY_DATABASE_URI,
                              SQLALCHEMY_TRACK_MODIFICATIONS)
from auth.extensions.flask import app

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)
