from auth.extensions.postgres import db
from flask_migrate import Migrate
from flask import Flask
from pathlib import Path
import os

directory = os.path.join(
    Path(__file__).parent.parent.absolute(),
    'migrations'
)


def init_migration(app: Flask):
    migrate = Migrate(
        app,
        db,
        directory=directory
    )
    return migrate
