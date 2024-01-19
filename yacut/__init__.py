from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from yacut.settings import Config
from yacut.constants import PRODUCTION_MODE


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import api_views, error_handlers, views
if app.env != PRODUCTION_MODE:
    db.create_all()