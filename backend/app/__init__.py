from flask import Flask
from .config import Config
from .extensions import db, jwt, bcrypt
from .routes import register_blueprints

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
