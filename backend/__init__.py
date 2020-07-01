from flask import Flask
from backend.config import FlaskConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)
flask_app.config.from_object(FlaskConfig)

db_app = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db_app)


from backend import routes