import logging
import argparse

from flask import Flask

from app.blueprints.kat.kat_backend import blueprint
from app.blueprints.kat.models.shared import db

API_ROOT = "/api/v2"

from app.config import ProductionConfig
print(ProductionConfig.AUTH_USERS)

def create_app(config="app.config.ProductionConfig"):
    log = logging.getLogger()
    handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
    log.addHandler(handler)
    a = Flask(__name__)
    a.config.from_object(config)
    db.init_app(a)
    a.register_blueprint(blueprint, url_prefix='/api/v2')
    return a


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("env", type=str, choices=['prod', 'dev'])
    args = ap.parse_args()

    configs = {
        'test': 'app.config_defaults.TestingConfig',
        'dev': 'app.config.DevelopmentConfig',
        'prod': 'app.config.ProductionConfig'
    }

    a = create_app(configs[args.env])
    a.run(debug=True, host="0.0.0.0")
