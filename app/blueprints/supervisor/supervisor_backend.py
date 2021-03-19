from flask import Blueprint
from flask_restful import Api

from app.blueprints.supervisor.resources.service import ServiceListResource, ServiceResource


blueprint = Blueprint("supervisor_backend", __name__)
api = Api(blueprint)

# Service Resources
api.add_resource(ServiceListResource, "/services", endpoint="services")
api.add_resource(ServiceResource, "/services/<str:id>", endpoint="service")
