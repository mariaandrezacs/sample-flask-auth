from flask import Flask
from flask_login import LoginManager

from .container import get_container
from .infrastructure.database import db
from .infrastructure.models import UserModel
from .interfaces.api import register_blueprints
from .interfaces.errors import register_error_handlers

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


def create_app(config_name="development"):
    from .config import DevelopmentConfig, ProductionConfig

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }

    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, DevelopmentConfig))

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "api.login"

    if app.config.get("AUTO_CREATE_TABLES"):
        with app.app_context():
            db.create_all()

    register_blueprints(app)
    register_error_handlers(app)

    app.container = get_container()

    return app
