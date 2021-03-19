import argparse
import logging

import markdown2
from flask import Flask, make_response, render_template
from flask_restful import Api, Resource

from app.blueprints.kat.kat_backend import blueprint
from app.blueprints.kat.models.shared import db
from app.blueprints.kat.common.utils import generate_help


API_ROOT = "/api/v2"


def create_app(config="app.config.ProductionConfig"):
    a = Flask(__name__)
    a.config.from_object(config)
    db.init_app(a)
    a.register_blueprint(blueprint, url_prefix=API_ROOT)

    api_home = Api(a)
    api_home.add_resource(ApiRootResource, API_ROOT, endpoint="help")
    return a


class ApiRootResource(Resource):
    def __init__(self):
        super(ApiRootResource, self).__init__()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(generate_help(), 200, headers)


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
