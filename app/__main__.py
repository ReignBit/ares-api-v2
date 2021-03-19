from flask import Flask

from app.blueprints.kat.kat_backend import blueprint
from app.blueprints.kat.models.shared import db

API_ROOT = "/api/v2"


def create_app(config):
    a = Flask(__name__)
    a.config.from_object(config)
    db.init_app(a)
    a.register_blueprint(blueprint, url_prefix='/api/v2')
    return a


if __name__ == "__main__":
    a = create_app("app.config.DevelopmentConfig")
    a.run(debug=True, host="0.0.0.0")
