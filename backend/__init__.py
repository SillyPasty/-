from flask import Flask
from backend.config import FlaskConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

flask_app = Flask(__name__)
flask_app.config.from_object(FlaskConfig)

CORS(flask_app)

db_app = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db_app)


from backend import routes