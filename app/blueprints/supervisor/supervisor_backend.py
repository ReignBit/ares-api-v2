from flask import Blueprint
from flask_restful import Api

import time
import requests

from app.blueprints.supervisor.resources.service import ServiceListResource, ServiceResource


blueprint = Blueprint("supervisor_backend", __name__)
api = Api(blueprint)

# Service Resources
api.add_resource(ServiceListResource, "/services", endpoint="services")
api.add_resource(ServiceResource, "/services/<string:id>", endpoint="service")

def supervisor_thread(app):
    while(True):
        with app.app_context() as a:
            time.sleep(1)
            print(a)

#             data = requests.get(f"localhost:{app.port}/api/v2/services")
#             if data.status_code == 200:
#                 for service in data['data']:
#                     if service['status'] and service['pid'] > -1:
#                         # If service is classed as alive with a pid
#                         # check if it's still alive.
#                         if not check_service_process(service):
#                             # If the pid is no longer valid, set to offline
#                             requests.put(f"localhost:{}")

                    