from backend import flask_app

from backend.router.officialUser import official_user_bp
from backend.router.order import order_bp
from backend.router.product import product_bp
from backend.router.user import user_bp
from backend.router.type import type_bp
from backend.router.statistics import statistic_bp
from backend.router.login import login_bp

flask_app.register_blueprint(official_user_bp)
flask_app.register_blueprint(order_bp)
flask_app.register_blueprint(product_bp)
flask_app.register_blueprint(user_bp)
flask_app.register_blueprint(type_bp)
flask_app.register_blueprint(statistic_bp)
flask_app.register_blueprint(login_bp)

