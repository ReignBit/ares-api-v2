import argparse

from flask import Flask

from app.blueprints.kat.kat_backend import blueprint
from app.blueprints.kat.models.shared import db

API_ROOT = "/api/v2"


def create_app(config="app.config.ProductionConfig"):
    a = Flask(__name__)
    a.config.from_object(config)
    db.init_app(a)
    a.register_blueprint(blueprint, url_prefix='/api/v2')
    return a


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    args = ap.parse_args()

    configs = {
        'test': 'app.config_defaults.TestingConfig',
        'dev': 'app.config.DevelopmentConfig',
        'prod': 'app.config.ProductionConfig'
    }

    a = create_app(configs[args.env])
    a.run(debug=True, host="0.0.0.0")
