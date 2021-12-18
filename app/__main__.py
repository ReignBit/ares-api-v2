import argparse
import logging
import threading

import markdown2
from flask import Flask, make_response, render_template
from flask_restful import Api, Resource

from app.blueprints.kat.kat_backend import blueprint as kat_blueprint
from app.blueprints.supervisor.supervisor_backend import blueprint as supervisor_blueprint
from app.blueprints.supervisor.supervisor_backend import supervisor_thread
from app.blueprints.kat.models.shared import db
from app.blueprints.kat.common.utils import generate_help


API_ROOT = "/api/v2"

watchdog = threading.Thread()

def create_app(process_group):
    global watchdog
    a = Flask(__name__)

    if process_group == "api-kat":
        config = "app.config.ProductionConfig"
    elif process_group == "api-yumi":
        config = "app.config.DevelopmentConfig"
    else:
        config = "app.config.TestingConfig"

    a.config.from_object(config)
    db.init_app(a)

    # Blueprint registration
    a.register_blueprint(kat_blueprint, url_prefix=API_ROOT)
    a.register_blueprint(supervisor_blueprint, url_prefix=API_ROOT)
    # watchdog = threading.Thread(target=supervisor_thread, args=(a,))
    # watchdog.start()

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

    a = create_app(config=configs[args.env])
    a.run(debug=True, host="0.0.0.0")
    watchdog.join()
